In this repository I will post my insights during experimenting with the Raspberry Pi Zero W.

## Contents

1. Preparing the Raspberry Pi
    * Access the Pi on Windows
    * Set a fixed IPv6 address
    * Accessing the internet via the OTG cable
2. Using a PiTFT display
3. Using sensors and other inputs
    * Research about API integration
    * Research about the temperature sensor
    * Research about the LCD display
    * Research about audio output via GPIO

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

With this settings the Pi is accessible from the host computer, but it does not have access to the internet yet. This is because the RNDIS driver creates an own virtual network on the host computer which is not visible to the main network and vice versa. I tried to overcome this by setting a fixed MAC address (thanks to [this tutorial](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=199588&p=1245602#p1245457) by adding the following line to the file `/etc/modprobe.d/g_ether.conf`. Replace xx with any hexadecimal numbers that don't match other MAC addresses on your network:

        options g_ether dev_addr=xx:xx:xx:xx:xx:xx
        
Unfortunately that didn't work, so for now I use the `wlan0` WiFi interface to connect to a hotspot.


## Using a PiTFT display

I use a [PiTFT Plus 2.8" capacitive touch display](https://www.adafruit.com/product/2298) to easily access the terminal on the Pi Zero. It connects directly to the GPIO pins, so it doesn't need an extra HDMI or USB port.

Unfortunately the [original AdaFruit tutorial](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install) didn't work due to certificate problems. I used [this script](https://forums.adafruit.com/viewtopic.php?f=24&t=54246&sid=19ba7b71b9dcca00a538d2da6d6121e3&start=15#p630193) proviced by AdaFruit support to install the PiTFT.


## Using sensors and other inputs

I want to make a little weather tamagotchi that can interact in the following ways:
* It can read the temperature of its environment by using a temperature sensor.
* It can poll the outside temperature by using open weather data.
* Depending on those two temperature variables (and possibly other weather variables) the device outputs algorithmic music.
* The device has a LCD display to indicate its state in a visual way.

A very handy website is [pinout.xyz](https://pinout.xyz/), which displays a RPi pinout with all harware and GPIO pin numbers and other useful information.

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

Wiring (MCP3008 pins counted from left to right and top to bottom):
* MCP3008 pin **1** and **2** to Pi 5V
* MCP3008 pin **3** and **8** to Pi GND
* MCP3008 pin **4** to Pi SPI0 SCLK (hardware pin 23) or Pi SPI1 SCLK (hardware pin 40)
* MCP3008 pin **5** to Pi SPI0 MISO (hardware pin 21) or Pi SPI1 MISO (hardware pin 35)
* MCP3008 pin **6** to Pi SPI0 MOSI (hardware pin 19) or Pi SPI1 MOSI (hardware pin 38)
* MCP3008 pin **7** to Pi SPI0 CE0 (hardware pin 24) or Pi SPI1 CE0 (hardware pin 12)
* One of the TMP36 outer pins to MCP3008 pin **1** (5V)
* The other of the TMP36 outer pins to MCP3008 pin **3** (GND)
* The TMP36 middle pin to MCP3008 pin **9**
* The 0.1 μF condensator between the TMP36 middle pin and the TMP36 GND pin

### Research about the LCD display

I already have an  LCD display laying around for about 3 years so I thought it would be nice to incorporate that. AdaFruit has a [tutorial](https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/wiring) on how to connect an LCD display directly on the GPIO pins. You could also connect it through a I2C bridge, but since I don't need many pins I decided to use this manner. Below is the wiring scheme for the LCD:

![LCD wiring schene](https://cdn-learn.adafruit.com/assets/assets/000/018/260/large1024/raspberry_pi_RaspberryPiRGB_bb.png)

Needed components:
* LCD display 16x2 characters
* **3362P** 10 kΩ variable potentiometer (or similar)

Wiring:
* LCD pin **1** (VSS) to Pi GND
* LCD pin **2** (VDD) to Pi 5V
* LCD pin **3** (V0) to the pontentiometer middle pin
* LCD pin **4** (RS) to Pi GPIO 27 (hardware pin 13)
* LCD pin **5** (RW) to Pi GND
* LCD pin **6** (E) to Pi GPIO 22 (hardware pin 15)
* LCD pin **11** (D4) to Pi GPIO 25 (hardware pin 22)
* LCD pin **12** (D5) to Pi GPIO 24 (hardware pin 18)
* LCD pin **13** (D6) to Pi GPIO 23 (hardware pin 16)
* LCD pin **14** (D7) to Pi GPIO 18 (hardware pin 12)
* LCD pin **15** (A) to Pi 5V
* LCD pin **16** (K) to Pi GND
* The potentiometer outer pin to Pi 5V
* The potentiometer inner pin to Pi GND

### Research about audio output via GPIO

Obviously I need a speaker.
