
import zmq
import time
import sys

from matrix_io.proto.malos.v1 import driver_pb2
from pyObj import Data
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
from callbacks import register_data_callback, driver_keep_alive
from mixer import Mixer

matrix_ip = '127.0.0.1' #IP of the matrix
gpio_port = 20049 #Port for the GPIO

context = zmq.Context()
socket = context.socket(zmq.PUSH)

socket.connect('tcp://{0}:{1}'.format(matrix_ip, gpio_port)) #Connect to zmq server

mixer = Mixer() #Open a sound mixer

audioToggleMute = 0 #Matrix GPIO pin 0
audioLevelDown = 1 #Matrix GPIO pin 0
audioLevelUp = 2 #Matrix GPIO pin 0
mikeToggleMute = 3 #Matrix GPIO pin 0

decreaseLevel = -2 #Reduces volume by x
increaseLevel = 2 #Increases volume by x

def config_gpio_read():
    """ Send driver configuration to Matrix """
    config = driver_pb2.DriverConfig()
    config.delay_between_updates = 0.1 #0.1 seconds
    config.timeout_after_last_ping = 5 #5 seconds
    socket.send(config.SerializeToString())


reset = True #Boolean to know if volume buttons is pressed
toggleMic = True #Boolean to know if mic button is pressed
toggleOut = True #Boolean to know if out button is pressed

ledContext = zmq.Context()
ledService = ledContext.socket(zmq.REQ)
ledService.connect ("tcp://localhost:1337")

def gpio_callback(msg):
    """
    Recieve the updated GPIO values and act upon the pressed button
    Will mute audio, change volume intensity and mute the microphone
    """
    data = io_pb2.GpioParams().FromString(msg[0])
    gpioValues = ('{0:016b}'.format(data.values))
    gpioValues = gpioValues[::-1]
    gpioValues = list(gpioValues)
    global ledService
    global reset
    global toggleMic
    global toggleOut
    if gpioValues[audioToggleMute] == '0' and toggleOut == True:
        #If the audio mute button is pressed mute the speakers and show audio mute leds
        if mixer.toggleOutMute():
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        elif not mixer._outMuted and mixer._inMuted:
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        else:
            #If nothing is muted reset the leds once.
            ledService.send_pyobj(Data(force=True))
        ledService.recv()
        #Toggle to know we are currently pressing the button.
        toggleOut = False
    elif gpioValues[audioLevelDown] == '0' and not mixer._outMuted and not mixer._inMuted:
        #If the audio level down button is pressed decrease the volume and show an animation
        mixer.setVolume(decreaseLevel)
        #Toggle to know when the volume button is pressed
        reset = False
        ledService.send_pyobj(Data("volume", int((18/100)*mixer._outLevel), loop=True))
        ledService.recv()
    elif gpioValues[audioLevelUp] == '0' and not mixer._outMuted and not mixer._inMuted:
        #If the audio level up button is pressed increase the volume and show an animation
        mixer.setVolume(increaseLevel)
        #Toggle to know when the volume button is pressed
        reset = False
        ledService.send_pyobj(Data("volume", int((18/100)*mixer._outLevel), loop=True))
        ledService.recv()
    elif gpioValues[mikeToggleMute] == '0' and toggleMic == True:
        #If the microphone mute button is pressed mute the microphone and show audio mute leds
        if mixer.toggleMike():
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        elif mixer._outMuted and not mixer._inMuted:
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        else:
            #If nothing is muted reset the leds once.
            ledService.send_pyobj(Data(force=True))
        ledService.recv()
        toggleMic = False
    elif reset == False:
        ledService.send_pyobj(Data())
        ledService.recv()
        reset = True
    elif toggleOut == False and gpioValues[audioToggleMute] == '1':
        toggleOut = True
    elif toggleMic == False and gpioValues[mikeToggleMute] == '1':
        toggleMic = True
                
        
if __name__ == "__main__":
    ioloop.install()
    #Keep the connection alive
    Process(target=driver_keep_alive, args=(matrix_ip, gpio_port, 1)).start()
    #Configure the gpio read interval
    config_gpio_read()
    #Connect to the Matrix GPIO server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    data_port = gpio_port + 3
    socket.connect('tcp://{0}:{1}'.format(matrix_ip, data_port))
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    stream = zmqstream.ZMQStream(socket)
    #Wait for a stream of data to come
    stream.on_recv(gpio_callback)
    #Loop
    ioloop.IOLoop.instance().start()
