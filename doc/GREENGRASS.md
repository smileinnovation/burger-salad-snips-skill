# Greengrass
We will assume that your Greengrass group is already created and a core device is also created.
Now create a new Thing in the AWS IoT Hub and download the certificates. Including the root certificate of Amazon.  
*Don't forget to add a subscription from your thing to your Greengrass Core or your IoT Hub.*  
Open the file `config.ini` in the `/var/lib/snips/skills/burger-salad-snips-skill` folder.  
You should see this:
```
[global]
extra=false
lang=en
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
To use greengrass put the `greengrass=false` setting to `true`.
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
janv. 10 17:38:33 raspberrypi snips-skill-server[30535]: INFO:snips_skill_server_lib::runner: [food][out] Greengrass is not enabled
```
