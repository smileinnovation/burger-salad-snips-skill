#/usr/bin/env bash -e

sudo chmod 777 /dev/vchiq
mkdir -p venv/bin/
ln -s /opt/movidius/virtualenv-python/bin/activate venv/bin/activate
. venv/bin/activate
echo "installing dependencies"
sudo pip3 install -r requirements
echo "done"
deactivate
