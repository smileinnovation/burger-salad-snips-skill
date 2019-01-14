# SAM
From now on the following steps are to be performed **IN YOUR COMPUTER** not in the Raspberry.  
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
You are done !
If you want to work with a greengrass core follow [this step](./GREENGRASS.md "Greengrass setup")
