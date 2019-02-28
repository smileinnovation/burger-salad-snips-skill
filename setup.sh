#! /bin/bash -xe

# Download openvino library for Raspberry Pi
if [ ! -d inference_engine_vpu_arm ]; then
    cd /tmp
    wget https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz
    tar xf l_openvino*.tgz
    cd -
    mv /tmp/inference_engine_vpu_arm .
    rm -rf /tmp/l_openvino*
fi

VENV=venv
# Checking if an env already exists, if not create one.
if [ ! -d "$VENV" ]
then
    PYTHON=`which python3`
    $PYTHON -mvenv $VENV
fi

. $VENV/bin/activate
pip3 install -r requirements
