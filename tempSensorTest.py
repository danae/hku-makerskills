import time
import Adafruit_GPIO.SPI as SPI
from Adafruit_MCP3008 import MCP3008
 
# Constants for the SPI connection
spi_port = 0
spi_device = 0
mcp = MCP3008(spi=SPI.SpiDev(spi_port,spi_device))
  
while True:
  channeldata = mcp.read_adc(0)
  volts = channeldata * (5.0 / 1024.0)
  temperature = (volts - 0.5) * 100.0
  print("Data = {}, Voltage = {:.3f} V, Temperature = {:.1f} °C".format(channeldata,volts,temperature))
  time.sleep(1)

