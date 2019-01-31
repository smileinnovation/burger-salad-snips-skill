#/usr/bin/env bash -e

mkdir -p OpenVINO
cd OpenVINO
wget https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz
tar xvf l_openvino_toolkit_ie_p_2018.5.445.tgz
rm l_openvino_toolkit_ie_p_2018.5.445.tgz
sed -i "s|<INSTALLDIR>|$(pwd)/inference_engine_vpu_arm|" inference_engine_vpu_arm/bin/setupvars.sh
echo "source inference_engine_vpu_arm/bin/setupvars.sh" >> ~/.bashrc
source inference_engine_vpu_arm/bin/setupvars.sh
sh inference_engine_vpu_arm/install_dependencies/install_NCS_udev_rules.sh
python3 -c 'import cv2; print(cv2.__version__)'

sudo pip3 install -r requirements
