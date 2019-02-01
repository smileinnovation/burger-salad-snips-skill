#! /bin/bash -xe

VENV=venv

if [ ! -d "$VENV" ]
then
    # install openvino fro Raspberry Pi
    if [ ! -d inference_engine_vpu_arm ]; then
        cd /tmp
        wget https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz
        tar xf l_openvino*.tgz
        cd -
        mv /tmp/inference_engine_vpu_arm .
        rm -rf /tmp/l_openvino*
    fi

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
	echo "could not find python"
    fi
    $PYTHON -mvenv $VENV

fi

echo "Activating env"
. $VENV/bin/activate
pip3 install --no-cache-dir -r requirements


