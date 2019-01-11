#!/usr/bin/env python3
# -*-: coding utf-8 -*-

import configparser
import io
import queue
from foodinference.foodinference import FoodInference
from hermes_python.hermes import Hermes
from utils import message
from utils import GGConnect

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

ALL_INTENTS = ["segar:quoi","segar:stop","segar:again","segar:start"]

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
            "Je vai analyser votre plat ! Mettez le sous mon oeil",
            "Je peux analyser votre plat ! placez le plat sous la camera et dites moi quand je peux analyser"
        ],
        "burger": "Je vois un hamburger",
        "salad": "Je vois une salade",
        "other": "Je vois rien, à l'aide.",
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
        print("Reading config file")
        config = read_configuration_file("config.ini")
        print("Done")
        extra = config["global"].get("extra", False)
        greengrass = config["global"].get("greengrass", False)
        self.message = message.Message(SKILL_MESSAGES, 'fr')
        if greengrass == "true":
            print("Greengrass is enabled")
            ggConnect = GGConnect.GGConnect(config["greengrass"].get("host", None),
                                            config["greengrass"].get("rootca", None),
                                            config["greengrass"].get("certpath", None),
                                            config["greengrass"].get("privatekeypath", None),
                                            config["greengrass"].get("thingname", None),
                                            maxRetries=config["greengrass"].get("maxretires", 10))
            gg = ggConnect.connectToGG()
            self.food = FoodInference(gg)
        else:
            print("Greengrass is not enabled")
            self.food = FoodInference()

def loop_new_question(hermes, order):
    hermes.publish_start_session_action('default', self.messages.get(order), ALL_INTENTS, True, custom_data=None)
            
def end(hermes, order):
    hermes.publish_end_session(intent_message.session_id, hermes.skill.message.get(order))

def callback(hermes, intent_message):
    if hermes.skill.food.isOn:
        result = hermes.skill.food.infer()
        hermes.publish_continue_session(intent_message.session_id, hermes.skill.message.get(result))
        loop_new_question(hermes, "encore")
    else:
        end(hermes, "unknown")
    
def again(hermes, intent_message):
    if hermes.skill.food.isOn:
        loop_new_question(hermes, "again")
    else:
        end(hermes, "unknown")

def over(hermes, intent_message):
    if hermes.skill.food.isOn:
        end(hermes, "stop")
    else:
        end(hermes, "unknown")
        
def startAssistant(hermes, intent_message):
    if hermes.skill.food.isOn:
        hermes.skill.food.isOn = True
        loop_new_question(hermes, "start")
    else:
        end(hermes, "unknown")
        
if __name__ == "__main__":
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("segar:quoi", callback)\
         .subscribe_intent("segar:stop", over)\
         .subscribe_intent("segar:again", again)\
         .subscribe_intent("segar:start", startAssistant)\
         .loop_forever()
