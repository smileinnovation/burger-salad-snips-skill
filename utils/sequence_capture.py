from io import BytesIO
import cv2 as cv
import sys
import numpy as np
import picamera
import picamera.array
import json

import GGConnect

ARGS                 = 244,244
camera               = picamera.PiCamera()
MODEL = 'graphs/mobilenetv2_1_00_224_burger_salad_2'

net = cv.dnn.readNet(MODEL+'.xml', MODEL+'.bin')

net.setPreferableBackend(cv.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

# open classes definition
classes = json.load(open(MODEL +'.json', 'r'))
classes = { v:k for k, v in classes.items() }

# make a first "forward" pass to make the model going in
# the stick memory
blank = np.zeros((224, 224, 3), np.uint8)
blank[:] = (255,255,255)
blob = cv.dnn.blobFromImage(blank)
net.setInput(blob)
net.forward()

def capture(topic=None, gg=None):
    """
    Will capture a picture from the Pi camera, resize it and infer on it.
    """
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    img = cv.imdecode(data,1)
    img = cv.resize(img, (224,224))
    blob = cv.dnn.blobFromImage(img, 1., (224, 224), (104, 117, 123), crop=False)
    net.setInput(blob)
    res = net.forward()
    res = res.flatten()
    print(res)
    out = np.argmax(res)
    print(out)
    try:
        if gg is not None:
            messageJson = json.dumps("Sees a {0}".format(classes[out]))
            gg.publishAsync(topic, messageJson, 0)
            print('Published topic %s: %s' % (topic, messageJson))
            return labels[output.argmax()]
        else:
            print(classes[out])
            return classes[out]
    except:
        print(sys.exc_info()[1])

camera.framerate = 14
camera.resolution = (640,480)
