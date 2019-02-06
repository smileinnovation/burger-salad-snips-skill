# coding: utf8
import sys
import time
import warnings
from utils import sequence_capture

class FoodInference:

    @classmethod
    def __init__(self, topic=None, gg=None):
        self.gg = gg
        self.topic = topic
        self.isOn = False
        
    @classmethod
    def infer(self):
        if self.gg is not None:
            inference = sequence_capture.capture(self.topic, self.gg)
        else:
            inference = sequence_capture.capture()
        return inference

if (__name__ == "__main__"):
    c = FoodInference();
    print(c.infer())
