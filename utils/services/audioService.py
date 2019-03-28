import zmq
import time
import sys
import rpyc
from matrix_io.proto.malos.v1 import driver_pb2
from pyObj import Data
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
from callbacks import register_data_callback, driver_keep_alive
from mixer import Mixer

matrix_ip = '127.0.0.1'
gpio_port = 20049
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect('tcp://{0}:{1}'.format(matrix_ip, gpio_port))
mixer = Mixer()
audioToggleMute = 0
audioLevelDown = 1
audioLevelUp = 2
mikeToggleMute = 3
decreaseLevel = -2
increaseLevel = 2

def config_gpio_read():
    config = driver_pb2.DriverConfig()
    config.delay_between_updates = 0.1
    config.timeout_after_last_ping = 5
    socket.send(config.SerializeToString())

reset = True
toggleMic = True
toggleOut = True

ledContext = zmq.Context()
ledService = ledContext.socket(zmq.REQ)
ledService.connect ("tcp://localhost:1337")

def gpio_callback(msg):
    data = io_pb2.GpioParams().FromString(msg[0])
    gpioValues = ('{0:016b}'.format(data.values))
    gpioValues = gpioValues[::-1]
    global ledService
    gpioValues = list(gpioValues)
    global reset
    global toggleMic
    global toggleOut
    if gpioValues[audioToggleMute] == '0' and toggleOut == True:
        if mixer.toggleOutMute():
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        elif not mixer._outMuted and mixer._inMuted:
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        else:
            ledService.send_pyobj(Data(force=True))
        ledService.recv()
        toggleOut = False
    elif gpioValues[audioLevelDown] == '0' and not mixer._outMuted and not mixer._inMuted:
        mixer.setVolume(decreaseLevel)
        reset = False
        ledService.send_pyobj(Data("volume", int((18/100)*mixer._outLevel), loop=True))
        ledService.recv()
    elif gpioValues[audioLevelUp] == '0' and not mixer._outMuted and not mixer._inMuted:
        mixer.setVolume(increaseLevel)
        reset = False
        ledService.send_pyobj(Data("volume", int((18/100)*mixer._outLevel), loop=True))
        ledService.recv()
    elif gpioValues[mikeToggleMute] == '0' and toggleMic == True:
        if mixer.toggleMike():
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        elif mixer._outMuted and not mixer._inMuted:
            ledService.send_pyobj(Data("mute", mixer._outMuted, mixer._inMuted, loop=True, force=True))
        else:
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
    Process(target=driver_keep_alive, args=(matrix_ip, gpio_port, 1)).start()
    config_gpio_read()
    #Process(target=register_data_callback, args=(gpio_callback, matrix_ip, gpio_port)).start()
    # Grab a zmq context, as per usual, connect to it, but make it a SUBSCRIPTION this time
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    # Connect to the base sensor port provided in the args + 3 for the data port
    data_port = gpio_port + 3
    
    # Connect to the data socket
    socket.connect('tcp://{0}:{1}'.format(matrix_ip, data_port))
    
    # Set socket options to subscribe and send off en empty string to let it know we're ready
    socket.setsockopt(zmq.SUBSCRIBE, b'')
    
    # Create the stream to listen to
    stream = zmqstream.ZMQStream(socket)
    
    # When data comes across the stream, execute the callback with it's contents as parameters
    stream.on_recv(gpio_callback)
    print('Connected to data publisher with port {0}'.format(data_port))

    # Start a global IO loop from tornado
    ioloop.IOLoop.instance().start()
    
