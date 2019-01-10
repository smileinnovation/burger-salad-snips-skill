#/usr/bin/env bash -e

mkdir -p venv/bin/
ln -s /opt/movidius/virtualenv-python/bin/activate venv/bin/activate
. venv/bin/activate
echo "installing dependencies"
pip install -r requirements
echo "done"
deactivate

