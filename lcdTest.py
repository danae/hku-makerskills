import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration
LCD_RS = 27
LCD_EN = 22
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_BACKLIGHT = 4

# Define LCD column and row size for 16x2 LCD
COLUMNS = 16
ROWS = 2

# Initialize the LCD using the pins above
lcd = LCD.Adafruit_CharLCD(LCD_RS,LCD_EN,LCD_D4,LCD_D5,LCD_D6,LCD_D7,COLUMNS,ROWS,LCD_BACKLIGHT)

# Print a two line message
lcd.message('Hello!\nraspberry')

