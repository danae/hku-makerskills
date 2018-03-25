import spidev
import time
 
spi = spidev.SpiDev()
spi.open(0,0)
  
def read_spi(channel):
  spidata = spi.xfer2([1,(8+channel)<<4,0])
  return ((spidata[1] & 3) << 8) + spidata[2]
       
try:
  while True:
    channeldata = read_spi(0)
    millivolts = round((channeldata * 5.0 / 1024),0)
    temperature = (millivolts - 500) / 10
    print("Voltage = {:.0f} mV, Temperatuur = {:.1f} °C".format(millivolts,temperature))
    time.sleep(1)
                                     
except KeyboardInterrupt:
  spi.close()
