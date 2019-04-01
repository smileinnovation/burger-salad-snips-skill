import time
import zmq
import sys
from snipsConfig import read_configuration_file
from LedRunner import LedRunner
from matrix_io.proto.malos.v1 import driver_pb2, io_pb2
from pyObj import Data
from zmq.eventloop import ioloop, zmqstream

class LedService():

    def __init__(self):
        self._numLeds = int(read_configuration_file("/var/lib/snips/skills/burger-salad-snips-skill/config.ini").get("matrixLeds", "18"))
        self._leds = []
        for led in range(self._numLeds):
            self._leds.append(self.setLed())
        self._socket = zmq.Context().socket(zmq.PUSH)
        self._socket.connect('tcp://127.0.0.1:20021')
        self._exec = LedRunner()
        self._muted = False
        self._breath = 0
        self._breathIn = True
        self._workingLed = 0
        self._switch = 0

    def setLed(self, **args):
        ledValue = io_pb2.LedValue()
        ledValue.red = args.get('red', 0)
        ledValue.green = args.get('green', 0)
        ledValue.blue = args.get('blue', 0)
        ledValue.white = args.get('white', 0)
        return ledValue

    def startup(self, speed=0.05):
        """
        Call this function when at startup.
        This animation will progressivly lit up the leds one by one to blue then green.
        This is a perpetual animation until it is stopped.
        """
        time.sleep(speed)
        if self._switch == 0:
            self._leds[self._workingLed] = self.setLed(blue=50)
        if self._switch == 1:
            self._leds[self._workingLed] = self.setLed(green=50)
        if self._workingLed < 17:
            self._workingLed += 1
        else:
            self._workingLed = 0
            self._switch = 1 if self._switch == 0 else 0
        self.send()

    def send(self):
        """Sends the led data to Matrix"""
        driver_config = driver_pb2.DriverConfig()
        driver_config.image.led.extend(self._leds)
        self._socket.send(driver_config.SerializeToString())

    def volume(self, num=0):
        """
        Shows x blue leds depending on % of volume
        """
        num = int(num)
        for led in range(num):
            self._leds[led] = self.setLed(blue=40)
        for led in range(self._numLeds-num):
            self._leds[led+num] = self.setLed()
        self.send()

    def listening(self, maxBrightness=100, speed=0.05):
        """
        Call this when the bot is listening.
        This animation will produce a blue 'breathing' effect.
        """
        time.sleep(speed)
        for led in range(self._numLeds):
            self._leds[led] = self.setLed(blue=10+self._breath)
        if self._breathIn:
            self._breath += 4
            if self._breath >= maxBrightness:
                self._breathIn = False
        else:
            self._breath -= 4
            if self._breath <= 0:
                self._breathIn = True
        self.send()
        
    def error(self):
        """
        Call this when an error is encountered.
        It will flash 2 times red light.
        """
        for led in range(self._numLeds):
            self._leds[led] = self.setLed(red=10)
        self.send()
        time.sleep(0.25)
        self.clear()
        time.sleep(0.25)
        for led in range(self._numLeds):
            self._leds[led] = self.setLed(red=10)
        self.send()
        time.sleep(0.25)
        self.clear()

    def mute(self, out, mic):
        """
        Lights up left and right leds to red when audio is muted
        Lights up bottom and top leds to blue when mic is muted
        """
        if out or mic:
            self._muted = True
        elif not out and not mic:
            self._muted = False
        for led in range(self._numLeds):
            self._leds[led] = self.setLed()
        if out:
            self._leds[2] = self.setLed(red=50)
            self._leds[3] = self.setLed(red=50)
            self._leds[4] = self.setLed(red=50)
            self._leds[5] = self.setLed(red=50)
            self._leds[6] = self.setLed(red=50)
            self._leds[11] = self.setLed(red=50)
            self._leds[12] = self.setLed(red=50)
            self._leds[13] = self.setLed(red=50)
            self._leds[14] = self.setLed(red=50)
            self._leds[15] = self.setLed(red=50)
        if mic:
            self._leds[0] = self.setLed(blue=50)
            self._leds[1] = self.setLed(blue=50)
            self._leds[7] = self.setLed(blue=50)
            self._leds[8] = self.setLed(blue=50)
            self._leds[9] = self.setLed(blue=50)
            self._leds[10] = self.setLed(blue=50)
            self._leds[16] = self.setLed(blue=50)
            self._leds[17] = self.setLed(blue=50)
        self.send()

    def working(self, speed=0.05, length=4):
        """
        Call this when processing information.
        The animation will produce incrementally lit 3 blue leds and 3 decrementally lit green leds.
        These 6 leds will turn around forever until they are stopped.
        """
        time.sleep(speed)
        for behind in range(1,length):
            bLed = (self._workingLed-behind) if (self._workingLed-behind) >= 0 else (18 + (self._workingLed-behind))
            if behind == 3:
                self._leds[bLed-1] = self.setLed(blue=0)
            else:
                self._leds[bLed] = self.setLed(blue=int(50/behind))
                
        for front in range(1,length):
            fLed = (self._workingLed+front) if (self._workingLed+front) <= 17 else ((self._workingLed+front) - 18)
            if front == 3:
                self._leds[fLed-1] = self.setLed(green=0)
            else:
                self._leds[fLed] = self.setLed(green=int(50/front))
        if self._workingLed < 17:
            self._workingLed += 1
        else:
            self._workingLed = 0
        self.send()

    def clear(self):
        """Turns all the leds off"""
        self._muted = False
        for led in range(self._numLeds):
            self._leds[led] = self.setLed()
        self.send()

    def ready(self):
        """
        Call this when bot is ready.
        It will flash 2 times all the green leds.
        """
        self.clear()
        time.sleep(0.5)
        for led in range(self._numLeds):
            self._leds[led] = self.setLed(green=50)
        self.send()
        time.sleep(1)
        self.clear()

    def exec(self, func, *args, force=False, loop=False):
        if loop and (not self._muted or force):
            print ("Loop")
            self._exec.start(getattr(self, func), *args)
        elif not self._muted or force:
            print ("Once")
            self._exec.once(getattr(self, func), *args)
        print ("END")

class LedServer():
    def __init__(self):
        self._socket = zmq.Context().socket(zmq.REP)
        self._socket.bind("tcp://*:1337")
        self._ledService = LedService()

    def start(self):
        while True:
            message = self._socket.recv_pyobj()
            print(message.action)
            self._ledService.exec(message.action, *message.args, loop=message.loop, force=message.force)
            self._socket.send_string("")

if __name__ == '__main__':
    print("Starting server")
    server = LedServer()
    server.start()
