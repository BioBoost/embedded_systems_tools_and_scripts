# Rpi Hello

Script sends json string using UDP broadcast with ip address and identifier.

## Listening for Hello's

This can be easily done using tcpdump and or ngrep (Network grep):

```shell
sudo ngrep -d eth0 -i "" udp port 1337 and ip broadcast
```

You may need to install ngrep using:
```shell
sudo apt-get install ngrep
```

The result should be something similar to this:

```shell
U 10.182.34.107:55436 -> 255.255.255.255:1337
  {"device": "Raspberry Pi 2", "ip address": "192.168.12.107", "identifier": "hello_universe", "mac address": "b8:27:eb:67:8f:33"}
```

## Injecting the rpi-hello project into an img for the pi

Make sure to change the identifier string before installing the rpi-hello service. The identifier can be found in the file identifier in the root dir.

Next you need to alter hello_injector.rb. Open it using nano or another text editor and edit the line of code `injector = HelloInjector.new "/home/bioboost/Downloads/2016-05-27-raspbian-jessie-lite.img", "/media/sf_VM_MINTYFRESH/rpi-hello"` at the bottom.
Make sure to enter the correct path of both the image file and the rpi project.

Next just execute the hello injector:

```shell
ruby hello_injector.rb
```