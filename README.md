# Burger Salad Snips Skill
  
You can find [french](https://console.snips.ai/app-editor/skill_x7VKk0K00Nyv "French version of the assistant") and [english](https://console.snips.ai/app-editor/skill_x7Vo5Y9kExaq "English version of the assistant") versions of the assistant.
  
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
  
## Movidius
  
To use the Movidius USB stick, you will need to install the SDK.  
Follow [this tutorial](https://movidius.github.io/ncsdk/virtualenv.html "Virtual environment installation tutorial") to install the ncsdk virtual environment.    
To check if everything works go in the *ncsdk/examples/apps/hello_ncs_py/* folder and run the *hello_ncs.py* script.
  
## CV2
  
To use this skill you will need to install the following packages and libraries.
```
sudo apt-get install python-opencv libjasper-dev libqtgui4 libqt4-test
``` 
## Pi Camera (if you are using it)
  
Activate the camera of the Pi by entering the following command:
```
sudo raspi-config
```
Select **5 Interfacing Options** -> **P1 Camera** then reboot the Pi
```
sudo reboot
```
  
You now need to give access to everyone to the folder */dev/vchiq*, so that the assistant can access the cameras images.
```
sudo chmod 777 /dev/vchiq
```
## Greengrass (not mandatory)

We will assume that your Greengrass group is already created and a core device is also created.  
Now create a new Thing in the AWS IoT Hub and download the certificates. Including the root certificate of Amazon.  
Open th file *config.ini* in the */var/lib/snips/skills/burger-salad-snips-skill* folder.  
You should see this:
```
[global]
extra=false
greengrass=false
[secret]
[greengrass]
# The endpoint
host=
# Path to the Amazon root certificate
rootca=
# Path to the thing certificate
certpath=
# Path to the private key of the thing
privatekeypath=
# Name of the thing
thingname=
# Number of attempts to discover a greengrass core.
maxretires=
```
To use greengrass put the **greengrass=false** setting to **true**.  
Now fill in the empty settings. The comments will help you know what you need to put.

Once every settings filled in, restart snips services:
```
sudo systemctl restart 'snips-*'
```

You are ready to go!
  
To check if everything works, do:
```
journalctl -f -u snips-skill-server
```
You should see this something like this:
```
janv. 10 17:38:30 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Done
janv. 10 17:38:30 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Loading graph
janv. 10 17:38:30 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Done
janv. 10 17:38:30 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Setting camera parameters
janv. 10 17:38:31 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Done
janv. 10 17:38:31 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Warming up the camera
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Done
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Reading config file
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][err] ./action-food.py:34: DeprecationWarning: The SafeConfigParser class has been renamed to ConfigParser in Python 3.2. This alias will b
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][err]   conf_parser = SnipsConfigParser()
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][err] ./action-food.py:35: DeprecationWarning: This method will be removed in future versions.  Use 'parser.read_file()' instead.
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][err]   conf_parser.readfp(f)
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Done
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Greengrass is not enabled
```
