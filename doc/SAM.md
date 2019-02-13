# SAM
Follow [these steps](https://snips.gitbook.io/getting-started/installation "Installing sam") to install sam on your computer and connect it to the Pi.
Once connected we will install snips to the Pi:
```
sam init
```
## Audio setup
Now plug in your speaker and microphone and setup with sam the audio for the Pi:
```
sam setup audio
```
Select `no` for `Is it a Snips Makers Kit?` select the input if needed and the output.
## Assistant installation
Now connect to your snips account with sam:
```
sam login
```
Once logged in install your assistant with either the [french](https://console.snips.ai/app-editor/skill_x7VKk0K00Nyv "French version of the assistant") or the [english](https://console.snips.ai/app-editor/skill_x7Vo5Y9kExaq "English version of the assistant") version of intents.
```
sam install assistant
```
Select the assistant.
You will need to reboot for the microphone to work.
```
sam reboot
```
Now you will need to setup the audio:
```
sam setup audio
```
Choose as a microphone the MATRIX. Then choose your speaker.
You are done !
  
If you want to work with Greengrass follow [this step](./GREENGRASS.md "Greengrass setup").  
Previous [step](./PI.md "Pi setup")  
[Menu](../README.md "Menu")
