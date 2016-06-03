# Hello World Loadable Kernel Module

This is simple loadable kernel module (LKM) that says (see kernel messages) "Hello Universe from the Kernel" when loaded and "ByeBye Universe from the Kernel" when unloaded.

It is also possible to provide a param 'name' when loading the module. This will change the text the module will output in the kernel messages.

It is meant to show the minimal code necessary to create a kernel module.

## Building the module on a Desktop pc

#### Linux Kernel Headers

You do need the linux header files for your current kernel version

TODO

### Actual building of the module

Create a symlink to the native makefile. For some reason the makefile has to be with a capital 'M' or it will not work.

```shell
ln -s makefile.native Makefile
```

Next execute a make

```shell
make
```

## Building the module for Raspberry Pi 2

Following are the required steps needed to compile and load the module on a Raspberry Pi 2.

### Required tools and dependencies

You will need the arm cross-compiler for the Raspberry Pi to be able to build the module. You can download the rpi-tools by cloning the github repository.

```shell
cd
git clone git@github.com:raspberrypi/tools.git rpi-tools
```

#### Linux Kernel Headers

Can be found at https://github.com/raspberrypi/linux

Kernel headers on a desktop system can be found at '/usr/src' and can be installed using apt-get.

### Actual building

## Loading the module

To load the module you can use the `insmod` command.

```shell
sudo insmod hello.ko
```

You can check if the module is loaded using `lsmod`.

To load the module with the `name` parameter set you use the following syntax:

```shell
sudo insmod hello.ko name='"Nico De Witte"'
```

Single and double quotes are required if name contains spaces. If only you only use double or single quotes they will get eaten by the shell and the module will think that multiple argumements are provided.

You can check parameter values by viewing `/sys/modules/hello/parameters/name`.

## Kernel messages

To see the message of the module run `dmesg`

```shell
dmesg
[ 8260.441767] NDW: Hello Universe from Kernel Space
```

## Unloading the module

To unload the module the `rmmod` command can be used

```shell
sudo rmmod hello.ko
```