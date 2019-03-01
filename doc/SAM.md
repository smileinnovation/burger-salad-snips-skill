# SAM
Follow [these steps](https://snips.gitbook.io/getting-started/installation "Installing sam") to install sam on your computer and connect it to the Pi.  
Once connected we will install snips to the Pi:
```
sam init
```
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
When prompt for `language` enter `en` or `fr` if you are using a french assistant.
And when prompt with `greengrass` enter `false` if you don't want to use it.
You will need to reboot for the microphone to work.
```
sam reboot
```
You will then need to connect to your Pi and manually launch a script.
For this go to `/var/lib/snips/skills/burger-salad-snips-skill/` and run this command:
```
sudo ./manual-setup.sh
```
Once everything has been installed reboot the pi and setup the audio.
  
## Audio setup
Now plug in your speaker and microphone and setup with sam the audio for the Pi:
```
sam setup audio
```
Select `no` for `Is it a Snips Makers Kit?` select the input if needed and the output.  
Choose as a microphone the MATRIX. Then choose your speaker.  
You are done !  
  
If you want to work with Greengrass follow [this step](./GREENGRASS.md "Greengrass setup").  
Previous [step](./PI.md "Pi setup")  
[Menu](../README.md "Menu")
