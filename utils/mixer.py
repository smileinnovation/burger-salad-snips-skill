import alsaaudio

class Mixer():
    """
    Mixer class that provides access to alsa in order to
    change the sounds parameters.
    """
    def __init__(self):
        self._outMixer = alsaaudio.Mixer("PCM")
        self._outLevel = self._outMixer.getvolume()[0] if self._outMixer.getvolume()[0] >= 0 else 0
        self._outMuted = self._outMixer.getmute()
        self._inMuted = False
        
    def toggleMike(self):
        """
        Mutes the microphone.
        """
	print("Mute microphone")
        if self._inMuted == False:
            publish.single("hermes/hotword/toggleOff", '{"sideId": "default"}', hostname="localhost:1883")
            TOGGLE = True
	else:
	    publish.single("hermes/hotword/toggleOn", '{"sideId": "default"}', hostname="localhost:1883")
	    TOGGLE = False

        
    def toggleOutMute(self):
        """
        Mutes/unmutes the audio output
        """
        if (self._outMuted):
            print("Unmuting")
        else:
            print("Muting")
        self._outMuted = True if self._outMuted == False else False
        self._outMixer.setmute(self._outMuted)

    def setVolume(self, value):
        """
        Sets the output volume - or + the value
        """
        newValue = self._outLevel + value
        print("Setting volume to {} dB".format(str(newValue)))
        if newValue < 50:
            newValue = 50
        elif newValue > 100:
            newValue = 100
        self._outMixer.setvolume(newValue)
        self._outLevel = newValue
