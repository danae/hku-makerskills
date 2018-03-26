import requests
import spidev
import time
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

  # Other constants
  lcd_columns = 16
  lcd_rows = 2

  # Constructor
  def __init__(self):
    # Create the SPI input
    self.spi = spidev.SpiDev()
    self.spi.open(0,0)

    # Create the LCD output
    self.lcd = LCD(self.lcd_rs,self.lcd_en,self.lcd_d4,self.lcd_d5,self.lcd_d6,self.lcd_d7,self.lcd_columns,self.lcd_rows)

  # Read a channel from the SPI device
  def read_spi(self, channel):
    spidata = self.spi.xfer2([1,(8+channel)<<4,0])
    return ((spidata[1] & 3) << 8) + spidata[2]

  # Poll the current internal temperature
  def poll_internal_temperature(self):
    channeldata = self.read_spi(0)
    voltage = round(channeldata * (5.0 / 1024.0),0)
    return (voltage - 500) / 10
  
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

  # Create a timer
  timer = 0
  state = -1

  try:
    # Main loop
    while True:
      # Poll data every half minute
      if timer % 30 == 0:
        # Get the temperatures
        location = "Kerkrade, NL"
        int_temp = device.poll_internal_temperature()
        ext_temp = device.poll_external_temperature(location)

        # Print to the console
        print(" Fetched data!")
        print("- Location: {}".format(location))
        print("- Internal temperature: {} °C".format(int_temp))
        print("- Outside temperature: {} °C".format(ext_temp))
        print()

      # Change the lcd state every 5 seconds
      if timer % 5 == 0:
        # Change the state
        state = (state + 1) % 2

        # Clear the display
        device.lcd.clear()

        # Print according to the state
        if state == 0:
            device.lcd.message("{0:^16}\n{1:^16}".format(time.strftime("%H:%M"),time.strftime("%d-%m-%Y")))
        elif state == 1:
          # Print temperatures
          device.lcd.message("Ext:  {0:>7.1f} {2}C\nInt:  {1:>7.1f} {2}C".format(ext_temp,int_temp,chr(0)))

      # Increase the timer
      timer += 1

      # Sleep for some time
      time.sleep(1.0)

  except KeyboardInterrupt:
    device.spi.close()

# Execute the main function
if __name__ == '__main__':
  main()
