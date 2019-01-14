# Pi installation

## Stretch installation

On a MicroSD, follow this [tutorial](https://www.raspberrypi.org/documentation/installation/installing-images/ "Raspbian Stretch installation tutorial") to install Raspbian Stretch.

## Camera and SSH setup

Once installed put the MicroSD card in the Raspberry Pi slot and plug an HDMI cable, a keyboard, a mouse, the [camera](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera "Camera installation tutorial") and the power to the Pi.  
Follow the instructions on the screen when it has booted.  
*Please note that you need an internet connection for the first installation process.*  
When the installation is done, open up the configuration panel:
```
sudo raspi-config
```
Select **5 Interfacing Options** -> **P1 Camera** activate it.
Select **5 Interfacing Options** -> **P2 SSH** and activate it.
Now you should reboot, if it asks you, select yes if it doesn't, do this command once you have exited the configuration panel:
```
sudo reboot
```
Once you rebooted give access to the folder `/dev/vchiq` to everyone. For that write this command:
```
sudo chmod 777 /dev/vchiq
```
Once rebooted open up a terminal and write:
```
ifconfig
```
Some text should show up, if you connected the Pi with the Wifi check the `inet` value at `wlan0` or `eth0` if you are connected with ethernet.
That is your Pi IP adress, write it somewhere we will need it later.  
Next [step](./MOVIDIUS.md "Movidius SDK installation").
