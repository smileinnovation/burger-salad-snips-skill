import alsaaudio
import paho.mqtt.publish as publish

class Mixer():
    """
    Mixer class that provides access to alsa in order to
    change the sounds parameters.
    """
    def __init__(self):
        self._outMixer = alsaaudio.Mixer("PCM")
        self._outLevel = self._outMixer.getvolume()[0] if self._outMixer.getvolume()[0] >= 0 else 90
        self._outMuted = self._outMixer.getmute()
        self._inMuted = False

    def toggleMike(self):
        """
        Mutes the microphone.
        """
        if self._inMuted == False:
            publish.single("hermes/hotword/toggleOff", '{"siteId": "default"}', hostname="localhost")
            publish.single("hermes/asr/stopListening", '{"siteId": "default"}', hostname="localhost")
            self._inMuted = True
        else:
            publish.single("hermes/hotword/toggleOn", '{"siteId": "default"}', hostname="localhost")
            self._inMuted = False

    def toggleOutMute(self):
        """
        Mutes/unmutes the audio output
        """
        self._outMuted = True if self._outMuted == False else False
        self._outMixer.setmute(self._outMuted)
        return self._outMuted

    def setVolume(self, value):
        """
        Sets the output volume - or + the value
        """
        newValue = self._outLevel + value
        if newValue < 0:
            newValue = 0
        elif newValue > 100:
            newValue = 100
        self._outMixer.setvolume(newValue)
        self._outLevel = newValue

