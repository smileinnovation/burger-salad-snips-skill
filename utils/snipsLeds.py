import paho.mqtt.client as mqtt
import json
import zmq
from pyObj import Data
from LedRunner import LedRunner


class LedControl:

    _SUB_ON_HOTWORD = 'hermes/hotword/default/detected'
    _SUB_ON_SAY = 'hermes/tts/say'
    _SUB_ON_THINK = 'hermes/asr/textCaptured'
    _SUB_ON_LISTENING = 'hermes/asr/startListening'
    _SUB_ON_HOTWORD_TOGGLE_ON = 'hermes/hotword/toggleOn'
    _SUB_ON_ERROR = 'hermes/nlu/intentNotRecognized'
    _SUB_ON_SUCCESS = 'hermes/nlu/intentParsed'
    _SUB_ON_PLAY_FINISHED = 'hermes/audioServer/default/playFinished'
    _SUB_ON_TTS_FINISHED = 'hermes/tts/sayFinished'

    '''
    _SUB_ON_LEDS_TOGGLE = 'hermes/leds/toggle'
    _SUB_ON_LEDS_TOGGLE_ON = 'hermes/leds/toggleOn'
    _SUB_ON_LEDS_TOGGLE_OFF = 'hermes/leds/toggleOff'
    _SUB_UPDATING = 'hermes/leds/systemUpdate'
    _SUB_ON_CALL = 'hermes/leds/onCall'
    _SUB_SETUP_MODE = 'hermes/leds/setupMode'
    _SUB_CON_ERROR = 'hermes/leds/connectionError'
    _SUB_ON_MESSAGE = 'hermes/leds/onMessage'
    _SUB_ON_DND = 'hermes/leds/doNotDisturb'
    '''

    def __init__(self, mqtt_host, mqtt_port):
        self._me = 'default'

        self._context = zmq.Context()
        self._runner = self._context.socket(zmq.REQ)
        self._runner.connect ("tcp://localhost:1337")
        self._runner.send_pyobj(Data("startup", loop=True))
        self._runner.recv()
        self.mqtt_client = None
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_client = self.connect()

    def on_connect(self, client, userdata, flags, rc):
        """
        Will connect and subscribe to hermes Snips topics.
        """
        self._runner.send_pyobj(Data("ready"))
        self._runner.recv()
        client.subscribe([
            (self._SUB_ON_HOTWORD, 0),
            (self._SUB_ON_SAY, 0),
            (self._SUB_ON_THINK, 0),
            (self._SUB_ON_LISTENING, 0),
            (self._SUB_ON_HOTWORD_TOGGLE_ON, 0),
            (self._SUB_ON_ERROR, 0),
            (self._SUB_ON_SUCCESS, 0),
            (self._SUB_ON_PLAY_FINISHED, 0),
            (self._SUB_ON_TTS_FINISHED, 0),
        ])

    def event_to_func(self, event):
        return {
            self._SUB_ON_HOTWORD:self.wakeup_event,
            self._SUB_ON_SAY:self.tts_start_event,
            self._SUB_ON_THINK: self.think_event,
            self._SUB_ON_LISTENING: self.listening_event,
            self._SUB_ON_HOTWORD_TOGGLE_ON: self.backtosleep_event,
            self._SUB_ON_ERROR: self.intent_error_event,
            self._SUB_ON_SUCCESS: self.intent_success_event,
            self._SUB_ON_PLAY_FINISHED: self.play_finished_event,
            self._SUB_ON_TTS_FINISHED: self.tts_finished_event
        }.get(event, self.unmanaged_event)

    def wakeup_event(self, payload):
        """
        Activate breathing effect when waking up.
        """
        self._runner.send_pyobj(Data("listening"))
        self._runner.recv()

    def backtosleep_event(self, payload):
        """
        Stop any effects when everything is done.
        """
        self._runner.send_pyobj(Data("clear"))
        self._runner.recv()

    def listening_event(self, payload):
        """
        Activate the breathing effect when listening.
        """
        self._runner.send_pyobj(Data("listening", loop=True))
        self._runner.recv()

    def think_event(self, payload):
        """
        Activate the working effect if an intent was found.
        Else, activate once the error effect.
        """
        likelihood = 0
        if payload is not None and 'likelihood' in payload:
            likelihood = payload['likelihood']

        if likelihood == 0:
            self._runner.send_pyobj(Data("error"))
            self._runner.recv()
        else:
            self._runner.send_pyobj(Data("working", loop=True))
            self._runner.recv()

    def tts_start_event(self, payload):
        pass

    def tts_finished_event(self, payload):
        pass

    def intent_error_event(self, payload):
        """
        When an error is encountered activate the error effect.
        """
        self._runner.send_pyobj(Data("error"))
        self._runner.recv()

    def intent_success_event(self, payload):
        """
        When success on an event, activate the ready effect.
        """
        self._runner.send_pyobj(Data("ready"))
        self._runner.recv()

    def play_finished_event(self, payload):
        pass

    def unmanaged_event(self, payload):
        """
        When an unmanaged event happens, activate the error effect. 
        """
        self._runner.send_pyobj(Data("error"))
        self._runner.recv()

    def on_message(self, client, userdata, message):
        if hasattr(message, 'payload') and message.payload:
            try:
                payload = json.loads(message.payload.decode('utf-8'))
                self.event_to_func(message.topic)(payload)
            except Exception as e:
                print(e)

    def connect(self):
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = self.on_connect
        mqtt_client.on_message = self.on_message
        return mqtt_client

    def start(self):
        self.mqtt_client.connect(self.mqtt_host, self.mqtt_port, 60)
        self.mqtt_client.loop_start()

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        self._runner.send_pyobj(Data("clear"))
        self._runner.recv()

if __name__ == '__main__':
    a = LedControl('localhost', 1883)
