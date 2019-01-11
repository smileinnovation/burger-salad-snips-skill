# Movidius setup

First you need to connect to your Pi:
```
pi@raspberrypi:~ $ ssh pi@<raspberry_ip_adress>
```
Write **yes** if you are prompt with *The authenticity of host 'xxx.xxx.xxx.xxx (xxx.xxx.xxx.xxx)' can't be established.*.
You should be in your Pi's home directory. We now will download the SDK:
```
pi@raspberrypi:~ $ git clone -b ncsdk2 http://github.com/Movidius/ncsdk && cd ncsdk
```
Now you are in the ncsdk folder. Open the ncsdk.config file:
```
pi@raspberrypi:~ $ nano ncsdk.conf
```
Change the value of **INSTALL_CAFFE** to **no** and the value of **USE_VIRTUALENV** to **yes**. Save the file and start the installation:
```
pi@raspberrypi:~/ncsdk $ make install
```