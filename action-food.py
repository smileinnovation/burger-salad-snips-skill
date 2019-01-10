#!/usr/bin/env python3
# -*-: coding utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from utils import message
from utils import GGConnect
import io
import queue
from foodinference.foodinference import FoodInference

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

SKILL_MESSAGES = {
    'fr': {
        "burger": "C'est un hamburger",
        "salad": "C'est une salade",
        "other": "C'est quelque chose",
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

def callback(hermes, intent_message):
    result = hermes.skill.food.infer()
    print(result)
    hermes.publish_end_session(intent_message.session_id, hermes.skill.message.get(result))
    
if __name__ == "__main__":
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("segar:quoi", callback).loop_forever()
