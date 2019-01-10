# Burger Salad Snips Skill
  
For this skill to work you will need to install beforehand a few libraries.  
  
## Movidius
  
To use the Movidius USB stick, you will need to install the SDK.  
We will assume you have a Raspberry with Raspbian Stretch.  
First make sure you have enough swap memory for the installation.  
To increase the swapfile size, edit the value of CONF_SWAPSIZE in /etc/dphys-swapfile:
```
sudo nano /etc/dphys-swapfile
```
The default value is 100 (MB). We recommend that you change this to 1024 (MB) or greater.  
Then restart the swapfile service:
```
sudo /etc/init.d/dphys-swapfile restart
```

Now we can proceed by cloning the ncsdk repository.
```
git clone -b ncsdk2 http://github.com/Movidius/ncsdk && cd ncsdk
```
Before installing you need to change the value of **USE_VIRTUALENV=no** in the file *ncsdk.conf* to **USE_VIRTUALENV=yes**.  
Now you can install the sdk.
  
```
make install
``` 
  
To check if everything works go in the *ncsdk/examples/apps/hello_ncs_py/* folder and run the *hello_ncs.py* script.

## Pi Camera (if you are using it)

Activate the camera of the Pi by entering the following command:
```
sudo raspi-config
```
Select **5 Interfacing Options** -> **P1 Camera** the reboot the Pi
```
sudo reboot
```
  
You now need to give access to everyone to the folder */dev/vchiq*, so that the virtual environment can access the cameras images.
```
sudo chmod 777 /dev/vchiq
```
## CV2
  
To use this skill you will need to install the following packages and libraries.
```
sudo apt-get install python-opencv libjasper-dev libqtgui4 libqt4-test
```
That is all for this.  
  
## Greengrass (not mandatory)

We will assume that your Greengrass group is already created and a core device is also created.
Transfer your certificate and greengrass core zip files to the Pi.
Unzip the files as explained in the tutorial of Greengrass.
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

Once every settings filled in restart snips services:
```
sudo systemctl restart 'snips-*'
```

You are ready to go!
