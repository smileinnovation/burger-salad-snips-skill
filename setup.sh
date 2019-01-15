#/usr/bin/env bash -e

mkdir -p venv/bin/
ln -s /opt/movidius/virtualenv-python/bin/activate venv/bin/activate
. venv/bin/activate
sudo pip3 install -r requirements
