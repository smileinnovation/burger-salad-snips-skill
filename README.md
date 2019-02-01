# Burger Salad Snips Skill
  
You can find a [french](https://console.snips.ai/app-editor/skill_x7VKk0K00Nyv "French version of the assistant") and [english](https://console.snips.ai/app-editor/skill_x7Vo5Y9kExaq "English version of the assistant") versions of intents for the assistant.
  
### How to use it
Just say **"Hey snips, I want you to analyze something"** and it will prompt you with what you have to do ! Easy.

# Installation notice
  
For this skill to work you will need to install beforehand a few libraries.  
  
## Requirements

- 1 Raspberry Pi 3 B
- 16 GB Micro SD card
- Raspbian Stretch installed on the Raspberry Pi [tutorial here](https://www.raspberrypi.org/documentation/installation/installing-images/ "Raspbian Stretch installation tutorial")
- 1 Movidius USB V1/V2
- 1 Raspberry Pi Camera V2.1
- 1 Microphone
- 1 Speaker

## Installation

- [Raspberry Pi](./doc/PI.md "Pi OS installation and setup")
- [Sam](./doc/SAM.md "sam installation")
- [Greengrass](./doc/GREENGRASS.md "Greengrass setup") (optional)

## Change language
  
To change the language (by default it is in english) to french, open the `config.ini` file in the folder `/var/lib/snips/skills/burger-salad-snips-skill`.
Replace `lang=en` to `lang=fr` and restart snips:
```
$> sudo systemctl restart 'snips-*'
```
## Known Issues
    
**Can not init USB device: NC_DEVICE_NOT_FOUND in function 'initPlugin'**: If you encounter this error first try to unplug and plug the USB device. If the error persists, you will need to do the following commands:  
Go to the folder where the skill is (usually located at `/var/lib/snips/skills/burger-salad-snips-skill`)
```
$> sudo cp "inference_engine_vpu_arm/deployment_tools/inference_engine/external/97-myriad-usbboot.rules" /etc/udev/rules.d/
$> sudo udevadm control --reload-rules
$> sudo udevadm trigger
$> sudo ldconfig
```
Now it should work.
