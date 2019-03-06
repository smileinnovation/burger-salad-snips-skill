import alsaaudio

class Mixer():
    """
    Mixer class that provides access to alsa in order to
    change the sounds parameters.
    """
    def __init__(self):
        self._outMixer = alsaaudio.Mixer("PCM")
        #self._inMixer = alsaaudio.Mixer()
        self._outLevel = self._outMixer.getvolume()[0]
        #self._inMuted = False
        self._outMuted = self._outMixer.getmute()

    #def toggleInMute(self):
        #"""
        #Mutes/Unmutes the microphone.
        #"""
        #self._inMuted = True if self._inmuted == False else False
        #self._inMixer.setmute(self._inMuted)

    def toggleOutMute(self):
        """
        Mutes/unmutes the audio output
        """
        self._outMuted = True if self._outMuted == False else False
        self._outMixer.setmute(self._outMuted)

    def setVolume(self, value):
        """
        Sets the output volume - or + the value
        """
        newValue = self._outLevel + value
        if newValue < 0:
            newValue = 0
        elif newValue > 90:
            newValue = 90
        self._outMixer.setvolume(newValue)
        self._outLevel = newValue
