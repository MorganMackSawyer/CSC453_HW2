import time
import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

def normalize_pot(value):
    pot_min = 10000
    pot_max = 60000
    return max(0.0, min(1.0, (value - pot_min) / (pot_max - pot_min)))

def normalize_ldr(value):
    ldr_min = 60
    ldr_max = 300
    return max(0.0, min(1.0, (value - ldr_min) / (ldr_max - ldr_min)))

#Define MCP3008 Port Numbers
potPORT = 7
ldrPORT = 0

# Setup SPI and MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP3008(spi, cs)

# Create channels (LDR on 0, Pot on 1 - adjust as needed)
ldr = AnalogIn(mcp, ldrPORT)
pot = AnalogIn(mcp, potPORT)

while True:
    # Read LDR
    ldr_value = ldr.value
    ldr_voltage = ldr.voltage
    
    # Read potentiometer  
    pot_value = pot.value
    pot_voltage = pot.voltage
    
    # Print results
    print(f"LDR: {ldr_value} | {ldr_voltage:.2f}V | POT: {pot_value} | {pot_voltage:.2f}V")
    norm_ldr_val = normalize_ldr(ldr_value)
    norm_pot_val = normalize_pot(pot_value)

    print("Normalized LDR Value: " +  str(norm_ldr_val))
    print("Normalized Pot Value: " + str(norm_pot_val))
    
    time.sleep(1)  # Wait 1 second