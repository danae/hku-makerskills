In this repository I will post my insights during experimenting with the Raspberry Pi Zero W.

## Preparing the Raspberry Pi

This section discusses installing the Pi and configure its networks so I can access the Pi from my host computer and vice versa, as well as connecting to the internet on the Pi.

### Access the Pi on Windows

First install the latest Raspbian Jessie from the Raspberry Pi website and update the packages (using `sudo apt update` and `sudo apt upgrade`). Now to access the Pi on a Windows machine, take the following steps:

1. Boot into the Pi using a display and keyboard.
2. Make sure an SSH server is running (use `raspi-config` to enable).
3. Add the following line to the file `/boot/config.txt`. This will load the correct USB driver in the kernel to use the Pi as an On-The-Go device:

```
dtoverlay=dwc2
```

4. Add the following lines to the file `/etc/modules`. This enables the modules to use the Pi as a virtual network device:

```
dwc2
g_ether
```

5. Reboot the Pi and connect an USB cable from the pc to the USB port of the Pi.

If the Pi isn't discovered as an *USB Ethernet/RNDIS Gadget*, then follow the steps on [this French website](http://domotique.caron.ws/cartes-microcontroleurs/raspberrypi/pi-zero-otg-ethernet/) to install the correct driver:

6. Download the RNDIS driver provided by the website and extract it.
7. In the Windows Device Manager, locate the Pi, right click on it and select *Properties*.
8. Install the driver by locating it with the *Install driver...*  option.

Now I can SSH into the Pi using its IPv6 address on the `usb0` interface, e.g.:

```shell
ssh pi@fe80::5563:28e9:b94e:8c3c%eth3
```

However every time the Pi boots the IPv6 address changes, due to the virtual network that is created, so I would like to use the hostname of the Pi to SSH into it or set a fixed IP address.

### Set a fixed IPv6 address

To set a fixed IPv6 address, add the following lines to the `/etc/dhcpcd.conf` file:

```
interface usb0
static ip_address=169.254.64.64
static ip6_address=fe80::40:40
```

Reboot the Pi. You can now SSH into the Pi using the IPv6 address:

```shell
ssh pi@fe80::40:40
```

For now this is the best solution, since Windows doesn't have any zeroconf or bonjour servces installed and the ones I tried don't work.

### Accessing the internet via the OTG cable

With this settings the Pi is accessible from the host computer, but it does not have access to the internet yet. This is because the RNDIS driver creates an own virtual network on the host computer which is not visible to the main network and vice versa. To overcome this, set a fixed MAC address by adding the following line to the file `/etc/modprobe.d/g_ether.conf`. Replace xx with any hexadecimal numbers that don't match other MAC addresses on your network:

        options g_ether dev_addr=xx:xx:xx:xx:xx:xx
        
(Thanks to [this tutorial](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=199588&p=1245602#p1245457).)


## Using sensors and other inputs

I want to make a little weather tamagotchi that can interact in the following ways:
* It can read the temperature of its environment by using a temperature sensor.
* It can poll the outside temperature by using open weather data.
* Depending on those two temperature variables (and possibly other weather variables) the device outputs algorithmic music.
* The device has a LCD display to indicate its state in a visual way.

### Research about API integration

For the outside temperature I use the [current weather API of openweathermap.org](http://openweathermap.org/current). I created a Python script to get the data, using the `requests` package:

```python
import requests

url = 'https://api.openweathermap.org/data/2.5/find?q={}'.format(query)
response = requests.get(url, params = {'appid': '6b1a98fea6d95bbb8239e5ab471d5dd7', 'units': 'metric'})
responseJson = response.json()

temperature = responseJson['list'][0]['main']
```

### Research about the temperature sensor

The temperature sensor is an analog sensor and the Pi Zero only has digital inputs, thus the circuit needs an ADC. Domotix.com has a [nice tutorial](http://domoticx.com/raspberry-pi-temperatuur-sensor-tmp36-gpiomcp3008/) on this topic. It uses the **MCP3008** IC for the analog to digital conversion and the **TMP36** temperature sensor. Below is the wiring scheme they use to connect the sensor to a Pi:

![TMP36 + MCP3008 wiring diagram](http://domoticx.com/wp-content/uploads/Raspberry-Pi-met-MCP3008-en-TMP36-schema-768x638.png)

Needed components:
* **TMP36** temperature sensor
* **MCP3008** integrated circuit
* 0.1 μF condensator
* Male-to-female jumper wires

### Research about the LCD display

I already have an  LCD display laying around for about 3 years so I thought it would be nice to incorporate that. Raspberrytips.nl has a [tutorial](https://raspberrytips.nl/16x2-lcd-display-gpio-rpi/) on how to connect an LCD display directly on the GPIO pins. You could also connect it through a I2C bridge, but since I don't need many pins I decided to use this manner. Below is the wiring scheme for the LCD:

![LCD wiring schene](https://cdn.raspberrytips.nl/wp-content/uploads/2016/11/lcd1602_schema-raspberry-pi-600x476.png)

Needed components:
* LCD display 16x2 characters
* **3362P** 10 kΩ variable potentiometer (or similar)

### Research about the speaker

Obviously I need a speaker.
