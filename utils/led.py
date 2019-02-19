import os
import zmq
import time
from LedRunner import LedRunner
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from zmq.eventloop import ioloop, zmqstream

matrix_ip = '127.0.0.1'
everloop_port = 20021
led_count = 18

def set_led(**args):
    ledValue = io_pb2.LedValue()
    ledValue.red = args.get('red', 0)
    ledValue.green = args.get('green', 0)
    ledValue.blue = args.get('blue', 0)
    ledValue.white = args.get('white', 0)
    return ledValue

class Leds:

    def __init__(self):
        self.image = []
        context = zmq.Context()
        self.socket = context.socket(zmq.PUSH)
        self.socket.connect('tcp://{0}:{1}'.format(matrix_ip, everloop_port))
        self.driver_config_proto = driver_pb2.DriverConfig()
        for led in range(led_count):
            self.image.append(set_led())
        self.driver_config_proto.image.led.extend(self.image)
        self.socket.send(self.driver_config_proto.SerializeToString())
        self.breath = 0
        self.breathIn = True
        self.workingLed = 0
        self.switch = 0

    def send(self):
        """Sends the led data to Matrix"""
        self.driver_config = driver_pb2.DriverConfig()
        self.driver_config.image.led.extend(self.image)
        self.socket.send(self.driver_config.SerializeToString())

    def listening(self, maxBrightness=100, speed=0.05):
        """
        Call this when the bot is listening.
        This animation will produce a blue 'breathing' effect.
        """
        time.sleep(speed)
        for led in range(led_count):
            self.image[led] = set_led(blue=10+self.breath)
        if self.breathIn:
            self.breath += 4
            if self.breath >= maxBrightness:
                self.breathIn = False
        else:
            self.breath -= 4
            if self.breath <= 0:
                self.breathIn = True
        self.send()
        
    def error(self):
        """
        Call this when an error is encountered.
        It will flash 2 times red light.
        """
        for led in range(led_count):
            self.image[led] = set_led(red=10)
        self.send()
        time.sleep(0.25)
        self.clear()
        time.sleep(0.25)
        for led in range(led_count):
            self.image[led] = set_led(red=10)
        self.send()
        time.sleep(0.25)
        self.clear()
        
    def clear(self):
        """Turns all the leds off"""
        for led in range(led_count):
            self.image[led] = set_led()
        self.send()
            
    def working(self, speed=0.05, length=4):
        """
        Call this when processing information.
        The animation will produce incrementally lit 3 blue leds and 3 decrementally lit green leds.
        These 6 leds will turn around forever until they are stopped.
        """
        time.sleep(speed)
        for behind in range(1,length):
            bLed = (self.workingLed-behind) if (self.workingLed-behind) >= 0 else (18 + (self.workingLed-behind))
            if behind == 3:
                self.image[bLed-1] = set_led(blue=0)
            else:
                self.image[bLed] = set_led(blue=int(50/behind))
                
        for front in range(1,length):
            fLed = (self.workingLed+front) if (self.workingLed+front) <= 17 else ((self.workingLed+front) - 18)
            if front == 3:
                self.image[fLed-1] = set_led(green=0)
            else:
                self.image[fLed] = set_led(green=int(50/front))
        if self.workingLed < 17:
            self.workingLed += 1
        else:
            self.workingLed = 0
        self.send()

    def ready(self):
        """
        Call this when bot is ready.
        It will flash 2 times all the green leds.
        """
        self.clear()
        time.sleep(0.5)
        for led in range(led_count):
            self.image[led] = set_led(green=50)
        self.send()
        time.sleep(1)
        self.clear()
        
    def startup(self, speed=0.05):
        """
        Call this function when at startup.
        This animation will progressivly lit up the leds one by one to blue then green.
        This is a perpetual animation until it is stopped.
        """
        time.sleep(speed)
        if self.switch == 0:
            self.image[self.workingLed] = set_led(blue=50)
        if self.switch == 1:
            self.image[self.workingLed] = set_led(green=50)
        if self.workingLed < 17:
            self.workingLed += 1
        else:
            self.workingLed = 0
            self.switch = 1 if self.switch == 0 else 0
        self.send()
        
if __name__ == '__main__':
    leds = Leds()
    runner = LedRunner()
    while True:
        a = input("$> ")
        if a == "working":
            runner.start(leds.clear)
            runner.start(leds.working)
        elif a == "error":
            runner.start(leds.clear)
            runner.start(leds.error)
        elif a == "clear":
            runner.start(leds.clear)
        elif a == "listening":
            runner.start(leds.clear)
            runner.start(leds.listening)
        elif a == "startup":
            runner.start(leds.clear)
            runner.start(leds.startup)
        elif a == "ready":
            runner.start(leds.clear)
            runner.once(leds.ready)
