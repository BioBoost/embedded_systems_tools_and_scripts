# Operating Systems

The Raspberry Pi foundation provides several ready to use operating system images for the Pi. At the moment of this writing the following are available:

* Raspbian - The Foundation's official supported operating system (Debian Jessie)
* Ubuntu Mate - Official Ubuntu flavor featuring the MATE desktop 
* Snappy Ubuntu Core - A new, transactionally-updated Ubuntu for IoT devices, clouds and more
* OSMC - Open Source Media Centre
* OPENELEC - Open Embedded Linux Entertainment Centre
* PINET - Raspberry Pi Classroom Management Solution
* Windows 10 IoT Core
* RISC OS - A non-Linux distribution

For this course we will be using the Raspbian image. While Ubuntu Mate features a nicer graphical environment it does however not currently offer a headless installation.

!!! note "Headless Installation"
    A headless machine is a machine without a keyboard, mouse and monitor. This means you need to be able to boot the machine to a state where you can remotely access it to finish the installation/configuration process.

While the instructions below on how to boot the Raspberry Pi are based on Raspbian, they are very similar for most other distributions.

## Creating a bootable SD card

You can download the latest image of Raspbian via the Raspberry Pi website ([https://www.raspberrypi.org/downloads/](https://www.raspberrypi.org/downloads/)). Make sure to pick the "Raspbian Jessie Lite" edition. Extract the compressed file on your local disk (using 7-Zip or a similar tool). You should get an image file (.img extension).

The current version at the moment of this writing is of May with a Linux kernel version of 4.4. You can always check out the release notes on [http://downloads.raspberrypi.org/raspbian/release_notes.txt](http://downloads.raspberrypi.org/raspbian/release_notes.txt). Do note that the lite edition does not include a graphical desktop environment. If this is required than download the normal image.

To boot this Linux distribution we will need to write the image file to an SD card of at least 4GB. A popular tool to write the image to an SD card is "Win32 Disk Imager" which can be downloaded at [http://sourceforge.net/projects/win32diskimager](http://sourceforge.net/projects/win32diskimager)

!!! note "Other host operating systems"
    Check out [http://www.raspberrypi.org/documentation/installation/installing-images/README.md](http://www.raspberrypi.org/documentation/installation/installing-images/README.md) for instructions for different host operating systems such as Linux or Mac.

Select the correct device letter and load the Linux image from your local drive as shown in the image below. If you're ready, hit the write button and grab a cup of coffee. You can also create a backup of your current SD card by reading from the SD card to an image file. Just make sure to select a new image file name. Do take note that the img file will have the size of your SD card. So using an SD card of 32GB will result in a backup image of 32GB.

![Win32 Disk Imager](img/win32_disk_imager.png)
:   Win32 Disk Imager

Once the write process is finished you can remove the SD card and plug it in the Raspberry Pi. Just make sure to disconnect the power before inserting the SD card.

If you want your Pi to be connected to your local area network (LAN), you will have to plug in the Ethernet cable before booting the Pi. The Pi is default configured to acquire an IP address using DHCP.

## Interacting with the Raspberry Pi

Booting the Raspberry Pi is really simple. All you have to do is fit in the SD card and plug in the supply adapter. It automatically boots from the SD card. Interacting with the Linux operating system from that point on can be a bit harder in certain situations.

### Graphical Desktop Environment

If you deployed an OS such as Raspbian than you can attach an HDMI display or RCA Video compatible device (yellow connector on the board). You will also have to connect a USB keyboard to the Pi to be able to control the Pi. Depending on the edition (normal or lite), you will get a graphical desktop environment or a tty terminal.

![Raspbian Graphical Desktop Environment](img/raspbian_gui.jpg)
:   Raspbian Graphical Desktop Environment

![Raspbian TTY Terminal](img/raspbian_tty.png)
:   Raspbian TTY Terminal

!!! warning "TODO"
    Jump to Section 3.3 to configure the Pi for initial use by means of the configuration menu.

### SSH Connection

Raspbian comes default with the SSH daemon enabled. This allows us to connect to the Pi from a remote computer using the SSH protocol. Before we can do this we will have to determine the IP address of the Pi. In case of a home network you can log on to your router and look for the last IP address that was given by your DHCP server running on the router.

!!! note "SSH"
    SSH or Secure Shell is a secure way to connect to a device and execute commands from a distance. In the old days Telnet was the way to go but it sends all commands and login information as clear text. With SSH everything is encrypted. Default SSH daemon listen on port 22. See chapter xxxx for more information on SSH.

Another option can be a network scan tool such as SoftPerfect Network Scanner (can be downloaded from [http://www.softperfect.com/products/networkscanner/](http://www.softperfect.com/products/networkscanner/)) which allows you to scan a range of IP addresses and display some basic information about them such as the MAC (Media Access Control) address and the hostname.

This would not be an option in a LAB if there are 12 Pi's connected to the same subnet all with the default configuration of Raspbian. However for your convenience we added labels on the Pi's with their respective MAC addresses so you can identify which Pi is yours.

![Network scan using SoftPerfect Network Scanner](img/network_scan.png)
:   Network scan using SoftPerfect Network Scanner

Another option is using WireShark and watch the communication on the network. Especially the DHCP traffic which distributes IP addresses to the connected client devices. This way you can also identify what IP address is given to your device (if you know the MAC address of your device).

!!! note "Wireshark"
    Wireshark, originally named Ethereal, is a free and open-source packet analyzer. It is used for network troubleshooting, analysis, software and communications protocol development, and education. It can be downloaded from [https://www.wireshark.org](https://www.wireshark.org).

Connecting to a device using the SSH protocol can be easily achieved using a terminal tool such as Putty. All you have to do is start Putty and select the SSH connection option and specify the IP address of the device as shown in Figure 6. Once the connection is configured you can open it.

!!! note "Putty"
    PuTTY is a free implementation of Telnet and SSH for Windows and Unix platforms, along with an xterm terminal emulator. It can be downloaded from [http://www.chiark.greenend.org.uk/~sgtatham/putty](http://www.chiark.greenend.org.uk/~sgtatham/putty).

![Opening an SSH connection using Putty](img/putty.png)
:   Opening an SSH connection using Putty

You will be presented with the command line interface (CLI) of the Linux operating system running on your device. The first thing you will see is a login screen similar to the one shown below.

![The login screen of the Raspbian distribution running on the Pi](img/cli_login.png)
:   The login screen of the Raspbian distribution running on the Pi

The default username and password can be found on the Raspberry Pi website. For Raspbian it is "pi" as username and "raspberry" as password. Once you login with these credentials you are presented with the command line interface as shown below. From this point on you can start to execute commands on the Pi.

![The command line interface after logging in](img/cli_after_login.png)
:   The command line interface after logging in

One of the most useful commands you should remember is the `ifconfig` command which displays the current network interfaces and their configuration parameters. If you execute the command you should get a similar output to the one shown in the figure below. Try to identify the IP address and MAC address of the primary Ethernet interface (eth0).

![Output of the ifconfig command](img/cli_ifconfig.png)
:   Output of the ifconfig command

### RS232 Connection

A last option that can be used to connect to the Raspberry Pi is using a serial connection. This is often used for debugging embedded systems because it is a very basic connection type. Because of this the kernel will also output its kernel messages (debugging information and errors) to this connection. Since most computers these days lack the serial interface we can use a simple RS232 to USB converter such as the PL-2303HX.

To attach the converter we do have to take a look at the pinout of the GPIO connector on the Raspberry Pi board, shown in the figure below.
