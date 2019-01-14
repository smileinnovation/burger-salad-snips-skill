# Movidius setup
  
On your computer, in a terminal, you need to connect to your Pi:
```
ssh pi@<raspberry_ip_adress>
```
Write `yes` if you are prompt with `The authenticity of host 'xxx.xxx.xxx.xxx (xxx.xxx.xxx.xxx)' can't be established.`.
You should be in your Pi's home directory. We will now download the SDK for Movidius:
```
git clone -b ncsdk2 http://github.com/Movidius/ncsdk && cd ncsdk
```
Now you are in the ncsdk folder. Open the `ncsdk.config` file:
```
nano ncsdk.conf
```
Change the value of `INSTALL_CAFFE` to `no` and the value of `USE_VIRTUALENV` to `yes`. Save the file and start the installation:
```
make install
```
  
Go grab a cup of coffee this will take a while.
  
To test if the installation was a success, plug in the Movidius USB and test a script:
```
source /opt/movidius/virtualenv-python/bin/activate
python examples/apps/hello_ncs_py/hello_ncs.py
```
You should see these messages:
```
Hello NCS! Device opened normally.
Goodbye NCS! Device closed normally.
NCS device working.
```
Next [step](./CV2.md "CV2 installation")
