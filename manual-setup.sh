#! /bin/bash -xe

#Updating repository list
curl -k https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update

#Checking if all the packages needed are installed
sudo apt-get install --yes python3-pip matrixio-malos gnome-schedule

#Setting config file for Matrix & Snips
sudo sed -i 's/# mike = "Built-in Microphone"/mike = "MATRIXIO SOUND: - (hw:2,0)"/g' /etc/snips.toml

#Giving snips access to USB ports and video feed.
sudo usermod -a -G video _snips-skills
sudo usermod -a -G users _snips-skills

# Updating udev rules
sudo cp "inference_engine_vpu_arm/deployment_tools/inference_engine/external/97-myriad-usbboot.rules" /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo ldconfig
