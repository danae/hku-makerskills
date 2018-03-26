import requests
import time
from Adafruit_GPIO.SPI import SpiDev as SPI
from Adafruit_MCP3008 import MCP3008
from Adafruit_CharLCD import Adafruit_CharLCD as LCD

# Weather device class
class WeatherDevice:
  # Constants for the Pi pins
  lcd_rs = 27
  lcd_en = 22
  lcd_d4 = 25
  lcd_d5 = 24
  lcd_d6 = 23
  lcd_d7 = 18

  # Constants for the SPI connection
  spi_port = 0
  spi_device = 0

  # Other constants
  lcd_columns = 16
  lcd_rows = 2

  # Constructor
  def __init__(self):
    # Create the MCP input
    self.mcp = MCP3008(spi=SPI(self.spi_port,self.spi_device))

    # Create the LCD output
    self.lcd = LCD(self.lcd_rs,self.lcd_en,self.lcd_d4,self.lcd_d5,self.lcd_d6,self.lcd_d7,self.lcd_columns,self.lcd_rows)

  # Poll the current internal temperature
  def poll_internal_temperature(self):
    channeldata = self.mcp.read_adc(0)
    volts = channeldata * (5.0 / 1024.0)
    return (volts - 0.5) * 100.0
  
  # Poll the current external temperature
  def poll_external_temperature(self, query = "Utrecht, NL"):
    url = "https://api.openweathermap.org/data/2.5/find?q={}".format(query)
    response = requests.get(url, params = {'appid': '6b1a98fea6d95bbb8239e5ab471d5dd7', 'units': 'metric'})
    responseJson = response.json()
    return responseJson['list'][0]['main']['temp']


# Main function
def main():
  # Create the weather device
  device = WeatherDevice()
  device.lcd.create_char(0,[12,18,18,12,0,0,0,0])

  # Create a timer and a state for the LCD
  timer = 0
  state = -1

  # Variables for data storage
  location = "Utrecht, NL"
  int_temp = 0
  ext_temp = 0

  # Main loop
  while True:
    # Poll API data every 30 seconds
    if timer % 30 == 0:
      ext_temp = device.poll_external_temperature(location)

    # Change state every 5 seconds
    if timer % 5 == 0:
      state = (state + 1) % 2

    # Pol lthe internal temperature
    int_temp = device.poll_internal_temperature()

    # Clear the display
    #device.lcd.clear()
    device.lcd.home()

    # Print according to the state
    if state == 0:
      # Print date and time
      device.lcd.message("{0:^16}\n{1:^16}".format(time.strftime("%H:%M:%S"),time.strftime("%d-%m-%Y")))
    elif state == 1:
      # Print temperatures
      device.lcd.message("Ext:  {0:>7.1f} {2}C\nInt:  {1:>7.1f} {2}C".format(ext_temp,int_temp,chr(0)))

    # Increase the timer
    timer += 1

    # Sleep for some time
    time.sleep(1.0)


# Execute the main function
if __name__ == '__main__':
  main()
