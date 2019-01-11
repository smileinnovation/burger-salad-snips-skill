# Movidius setup
  
First you need to connect to your Pi:
```
pi@raspberrypi:~ $ ssh pi@<raspberry_ip_adress>
```
Write `yes` if you are prompt with `The authenticity of host 'xxx.xxx.xxx.xxx (xxx.xxx.xxx.xxx)' can't be established.`.
You should be in your Pi's home directory. We now will download the SDK:
```
pi@raspberrypi:~ $ git clone -b ncsdk2 http://github.com/Movidius/ncsdk && cd ncsdk
```
Now you are in the ncsdk folder. Open the `ncsdk.config` file:
```
pi@raspberrypi:~ $ nano ncsdk.conf
```
Change the value of `INSTALL_CAFFE` to `no` and the value of `USE_VIRTUALENV` to `yes`. Save the file and start the installation:
```
pi@raspberrypi:~/ncsdk $ make install
```
  
Go grab a cup of coffee this will take a while.
  
To test if the installation was a success, plug in the Movidius USB and test a script:
```
pi@raspberrypi:~/ncsdk $ source /opt/movidius/virtualenv-python/bin/activate
(virtualenv-python) pi@raspberrypi:~/ncsdk $ python examples/apps/hello_ncs_py/hello_ncs.py
```
You should see these messages:
```
Hello NCS! Device opened normally.
Goodbye NCS! Device closed normally.
NCS device working.
```
Next step [CV2 installation](./CV2.md "CV2 installation")