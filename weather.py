import requests
import spidev
from Adafruit_CharLCD import Adafruit_CharLCD as LCD

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

# Poll the current external temperature
def pollExternalTemperature(query = 'Utrecht,NL'):
  # Make the request
  url = 'https://api.openweathermap.org/data/2.5/find?q={}'.format(query)
  response = requests.get(url, params = {'appid': '6b1a98fea6d95bbb8239e5ab471d5dd7', 'units': 'metric'})
  responseJson = response.json()
  temperature = responseJson['list'][0]['main']

  # Return it
  return temperature


# Main function
def main():
  # Create the LCD output
  lcd = LCD(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows)

  # Get the external temperature
  location = 'Kerkrade, NL'
  extTemp = pollExternalTemperature(location)['temp']

  # Print to the LCD
  lcd.message('Ext:  {:.1f} {}C'.format(extTemp,chr(223)))

# Execute the main function
if __name__ == '__main__':
  main()
