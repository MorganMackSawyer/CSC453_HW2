import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

#Define MCP3008 Port Numbers
potPORT = 7
ldrPORT = 0

# Setup SPI and MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP3008(spi, cs)

# Create channels (LDR on 0, Pot on 1 - adjust as needed)
ldr = AnalogIn(mcp, potPORT)
pot = AnalogIn(mcp, ldrPORT)

while True:
    # Read LDR
    ldr_value = ldr.value
    ldr_voltage = ldr.voltage
    
    # Read potentiometer  
    pot_value = pot.value
    pot_voltage = pot.voltage
    
    # Print results
    print(f"LDR: {ldr_value} | {ldr_voltage:.2f}V | POT: {pot_value} | {pot_voltage:.2f}V")
    
    time.sleep(1)  # Wait 1 second