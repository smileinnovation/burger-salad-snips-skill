#!/usr/bin/env python3
import os
import cv2
import sys
import io
import time
import numpy
import ntpath
import argparse
import picamera
import picamera.array
import mvnc.mvncapi as mvnc
import threading
import datetime
import json

from utils import GGConnect
from utils import visualize_output
from utils import deserialize_output

CONFIDANCE_THRESHOLD = 0.60 # 60% confidant
ARGS                 = 244,244
camera               = picamera.PiCamera()
done = False
lock = threading.Lock()
pool = []
labels = ["burger", "other", "salad"]

def open_ncs_device():
    print("Searching for device")
    devices = mvnc.enumerate_devices()
    if len( devices ) == 0:
        print( "No devices found" )
        quit()
    print("Found one")
    device = mvnc.Device( devices[0] )
    print("Accessing device")
    device.open()
    print("Done")
    return device

def load_graph(device):
    print("Loading graph")
    graph_filepath = './model/graph'
    with open(graph_filepath, 'rb') as f:
        graph_buffer = f.read()
    print("Done")
    return graph_buffer

def capture(gg=None):
    print("Called capture()")
    stream = picamera.array.PiRGBArray(camera)
    camera.capture(stream, format='rgb', use_video_port=True)
    stream.seek(0)
    frame = stream.array
    img = cv2.resize(frame, (224,224)).astype(numpy.float32)
    img = numpy.array(img)
    img = numpy.expand_dims(img, axis=0)
    input_fifo.write_elem(img, None)
    graph.queue_inference(input_fifo, output_fifo)
    print("Predicting ...")
    output, userobj = output_fifo.read_elem()
    try:
        if gg is not None:
            messageJson = json.dumps("Sees a {0}".format(labels[output.argmax()]))
            gg.publishAsync("gg/inference/food", messageJson, 0)
            print('Published topic %s: %s' % ("gg/inference/food", messageJson))
            return labels[output.argmax()]
        else:
            return labels[output.argmax()]
    except:
        print(sys.exc_info()[1])

device = open_ncs_device()
graph = mvnc.Graph('graph1')
input_fifo, output_fifo = graph.allocate_with_fifos(device, load_graph(device))
print("Setting camera parameters")
camera.framerate = 14
camera.resolution = (640,480)
print("Done")
print("Warming up the camera")
time.sleep(2)
print("Done")
