# rpi-discoveries

In this repository I will post my insights during experimenting with the Raspberry Pi Zero W.

## Access the Pi on Windows 10

The goal is to be able to access the shell of the Pi in *Bash on Ubuntu on Windows* using only an USB cable.

1. Install the latest Raspbian Jessie from the Raspberry Pi website.
2. Boot into the Pi using a display and keyboard and make sure an SSH server is running (use `raspi-config` to enable).
3. Add the line `dtoverlay=dwc2` to the file `/boot/config.txt`. This will load the correct USB driver in the kernel to use the Pi as an On-The-Go device.
4. Add the following lines to the file `/etc/modules`. This enables the modules to use the Pi as a virtual network device:

        dwc2
        g_ether
        
5. Reboot the Pi and connect an USB cable from the pc to the USB port of the Pi.
6. If the Pi isn't discovered as an *USB Ethernet/RNDIS Gadget*, then follow the steps on [this French website](http://domotique.caron.ws/cartes-microcontroleurs/raspberrypi/pi-zero-otg-ethernet/) to install the correct driver.

No I can SSH into the Pi using its IPv6 address on the `usb0` interface, e.g.:

        ssh pi@fe80::5563:28e9:b94e:8c3c%eth3
        
However every time the Pi boots the IPv6 address changes, so I would like to use the hostname of the Pi to SSH into it or set a fixed IP address.

## Set a fixed IPv6 address

To set a fixed IPv6 address, add the following lines to the `/etc/dhcpcd.conf` file:

        interface usb0
        static ip_address=169.254.64.64
        static ip6_address=fe80::40:40
        
Reboot the Pi. You can now SSH into the Pi using the IPv6 address:

        ssh pi@fe80::40:40

For now this is the best solution, since Windows doesn't have any zeroconf or bonjour servces installed and the ones I tried don't work.
