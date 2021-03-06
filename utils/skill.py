#!/usr/bin/env python3

from snipsLeds import LedControl

#Initialize this first in order to have the loading animation
ledControl = LedControl('localhost', 1883)

import time
import configparser
import io
import queue
from foodinference import FoodInference
from hermes_python.hermes import Hermes
import message
import GGConnect
import zmq
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop
from mixer import Mixer

matrix_ip = '127.0.0.1'
gpio_port = 20049
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect('tcp://{0}:{1}'.format(matrix_ip, gpio_port))
mikeToggleMute = 3

TOGGLE = False

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "../config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

ALL_INTENTS = ["segar:what","segar:stop","segar:again","segar:start"]

SKILL_MESSAGES = {
    'fr': {
        "encore":[
            "Vous voulez que je regarde à nouveau ?",
            "Je peux refaire une analyse si vous le voulez.",
            "Je refait une analyse ?"
        ],
        "again":[
            "Ok, mettez un plat près de mon oeil",
            "J'attends vos ordres",
            "ok, c'est reparti. Dites moi quand je dois analyser"
        ],
        "stop":[
            "Aurevoir !",
            "A bientôt !"
        ],
        "start":[
            "Je vais analyser votre plat ! Mettez le sous mon oeil",
            "Je peux analyser votre plat ! placez le plat sous la camera et dites moi quand je peux analyser"
        ],
        "unknown":[
            "J'ai pas compris",
            "Je ne connais pas cette commande"
        ],
        "ok":[
            "ok",
            "Un instant"
        ],
        "burger": "Je vois un hamburger",
        "green-salad": "Je vois une salade",
        "other": "Je vois rien, à l'aide.",
    },
    'en': {
        "encore":[
            "You want me to look again?",
            "I can analyze it again if you want",
            "Should I make an other analyze"
        ],
        "again":[
            "Ok, put a dish near my eye",
            "Awaiting orders",
            "ok, here we go again, tell me when you are ready"
        ],
        "stop":[
            "Bye",
            "See you soon"
        ],
        "start":[
            "I will analyze your plate, put it under my eye",
            "I can analyze your dish ! Tell me when you're ready"
        ],
        "unknown":[
            "I didn't understand",
            "I don't understand that command"
        ],
        "ok":[
            "ok",
            "a moment please"
        ],
        "burger": "I see a burger",
        "green-salad": "I see a salad",
        "other": "I can't see anything, help.",
    }
}

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

class Skill:
    def __init__(self):
        config = read_configuration_file("config.ini")
        lang = config["global"].get("lang", "en")
        greengrass = config["global"].get("secret", False)
        self.message = message.Message(SKILL_MESSAGES, lang)
        if greengrass == "true":
            print("Greengrass is enabled")
            ggConnect = GGConnect.GGConnect(config["secret"].get("host", None),
                                            config["secret"].get("rootca", None),
                                            config["secret"].get("certpath", None),
                                            config["secret"].get("privatekeypath", None),
                                            config["secret"].get("thingname", None),
                                            maxRetries=config["secret"].get("maxretires", 10))
            gg = ggConnect.connectToGG()
            self.food = FoodInference(config["secret"].get("topic", None),gg)
        else:
            print("Greengrass is not enabled")
            self.food = FoodInference()

def loop_new_question(hermes, order):
    hermes.publish_start_session_action('default', hermes.skill.message.get(order), ALL_INTENTS, True, custom_data=None, session_init_send_intent_not_recognized=hermes.skill.message.get("unknown"))
            
def end(hermes, order, intent_message):
    hermes.publish_end_session(intent_message.session_id, hermes.skill.message.get(order))

def callback(hermes, intent_message):
    """
    Makes an inference when the intent is to make a prediction.
    """
    if hermes.skill.food.isOn:
        result = hermes.skill.food.infer()
        hermes.publish_end_session(intent_message.session_id, hermes.skill.message.get(result))
        loop_new_question(hermes, "encore")
    else:
        end(hermes, "unknown", intent_message)

def again(hermes, intent_message):
    """
    Prepare for an other prediction.
    """
    if hermes.skill.food.isOn:
        end(hermes, "ok", intent_message)
        loop_new_question(hermes, "again")
    else:
        end(hermes, "unknown", intent_message)

def over(hermes, intent_message):
    """
    Stop everything.
    """
    if hermes.skill.food.isOn:
        hermes.skill.food.isOn = False
        end(hermes, "stop", intent_message)
    else:
        end(hermes, "unknown", intent_message)

def startAssistant(hermes, intent_message):
    """
    Start the assistant that makes predictions.
    """
    if not hermes.skill.food.isOn:
        hermes.skill.food.isOn = True
        end(hermes, "ok", intent_message)
        loop_new_question(hermes, "start")
    else:
        end(hermes, "unknown", intent_message)

if __name__ == "__main__":
    ioloop.install()
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("segar:what", callback)\
         .subscribe_intent("segar:stop", over)\
         .subscribe_intent("segar:again", again)\
         .subscribe_intent("segar:start", startAssistant)
        ledControl.start()
        h.loop_forever()
