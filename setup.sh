#/usr/bin/env bash -e

mkdir -p venv/bin/
ln -s /opt/movidius/virtualenv-python/bin/activate venv/bin/activate
pip install AWSIoTPythonSDK --user
pip install hermes-python --user
