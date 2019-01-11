# Burger Salad Snips Skill
  
You can find [french](https://console.snips.ai/app-editor/skill_x7VKk0K00Nyv "French version of the assistant") and [english](https://console.snips.ai/app-editor/skill_x7Vo5Y9kExaq "English version of the assistant") versions of intents for the assistant.
  
### How to use it
Just say **"Hey snips, I want you to analyze something"** and it will prompt you with what you have to do ! Easy.

# Installation notice
  
For this skill to work you will need to install beforehand a few libraries.  
  
## Requirements

- 1 Raspberry Pi 3 B
- 16 GB Micro SD card
- Raspbian Stretch installed on the Raspberry Pi [tutorial here](https://www.raspberrypi.org/documentation/installation/installing-images/ "Raspbian Stretch installation tutorial")
- 1 Movidius USB (V1 or V2)
- 1 Camera (we used Raspberry Pi Camera V2.1)
- 1 Microphone
- 1 Speaker

## Installation

- [Raspberry Pi](./doc/PI.md "Pi OS installation and setup")
- [Movidius](./doc/MOVIDIUS.md "Movidius installation and setup")
- [Sam](./doc/SAM.md "sam installation")
- [Greengrass](./doc/GREENGRASS.md "Greengrass setup") (optional)

## Change language
  
To change the language (by default it is in english) to french for example, open the `config.ini` file in the repository `/var/lib/snips/skills/burger-salad-snips-skill`.
Replace `lang=en` to `lang=fr` and restart snips:
```
$> sudo systemctl restart 'snips-*'
```
