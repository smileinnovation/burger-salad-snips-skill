#! /bin/bash -xe

#Updating repository list
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
sudo apt-get update

#Checking if all the packages needed are installed
./utils/check_package.sh matrixio-kernel-modules python3-pip matrixio-malos matrixio-creator-init libmatrixio-creator-hal libmatrixio-creator-hal-dev

#Setting config file for Matrix & Snips
sudo sed -i 's/# mike = "Built-in Microphone"/mike = "MATRIXIO SOUND: - (hw:2,0)"/g' /etc/snips.toml

#Giving snips access to USB ports and video feed.
sudo usermod -a -G video _snips-skills
sudo usermod -a -G users _snips-skills

# install openvino fro Raspberry Pi
if [ ! -d inference_engine_vpu_arm ]; then
    cd /tmp

    # Downloading openvino package & untarring it
    wget https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz
    tar xf l_openvino*.tgz
    cd -

    # Move openvino folder to the current folder
    mv /tmp/inference_engine_vpu_arm .
    rm -rf /tmp/l_openvino*

    # Updating udev rules
    sudo cp "inference_engine_vpu_arm/deployment_tools/inference_engine/external/97-myriad-usbboot.rules" /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    sudo ldconfig
fi



VENV=venv

# Checking if an env already exists, if not create one.
if [ ! -d "$VENV" ]
then
    PYTHON=`which python3`
    $PYTHON -mvenv $VENV
fi

echo "Activating env"
. $VENV/bin/activate

pip3 install -r requirements
