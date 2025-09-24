#Current Implementation of Pi w/ breadboard + ADC + Potentiometer
# Install the modern library (recommended)
#pip3 install adafruit-circuitpython-mcp3xxx
##
 # Maker's Digest
 #
 # MCP3008 ADC Example - Modernized for Python 3
 #
 # Install required libraries: pip3 install adafruit-circuitpython-mcp3xxx
##
import sys                      # Import sys module
from time import sleep          # Import sleep from time
import busio                    # Modern busio for SPI
import digitalio                # For digital controls
import board                    # Board pin definitions

# Import modern MCP3008 library
try:
    import adafruit_mcp3xxx.mcp3008 as MCP
    from adafruit_mcp3xxx.analog_in import AnalogIn
    MODERN_LIB = True
except ImportError:
    # Fallback to old library with updated import style
    try:
        import Adafruit_GPIO.SPI as SPI
        import Adafruit_MCP3008
        MODERN_LIB = False
    except ImportError:
        print("Error: Required libraries not installed.")
        print("Install with: pip3 install adafruit-circuitpython-mcp3xxx")
        sys.exit(1)

# Configuration
SPI_TYPE = 'HW'
dly = 0.5         # Delay of 500ms (0.5 second)

# Pin configurations (using modern board pin references)
if MODERN_LIB:
    # Modern library uses board pin definitions
    CLK_PIN = board.SCK    # Serial Clock
    MISO_PIN = board.MISO  # Master Input/Slave Output  
    MOSI_PIN = board.MOSI  # Master Output/Slave Input
    CS_PIN = board.D5      # Chip Select (adjust as needed)
else:
    # Legacy pin configurations (BCM numbering)
    CLK = 18    # Set the Serial Clock pin
    MISO = 23   # Set the Master Input/Slave Output pin
    MOSI = 24   # Set the Master Output/Slave Input pin
    CS = 25     # Set the Slave Select

# Hardware SPI Configuration
HW_SPI_PORT = 0 # Set the SPI Port. Raspi has two.
HW_SPI_DEV  = 0 # Set the SPI Device

# Initialize MCP3008 based on available library
if MODERN_LIB:
    # Modern library initialization
    try:
        # Create SPI bus
        spi = busio.SPI(clock=CLK_PIN, MISO=MISO_PIN, MOSI=MOSI_PIN)
        # Create chip select
        cs = digitalio.DigitalInOut(CS_PIN)
        # Create MCP3008 object
        mcp = MCP.MCP3008(spi, cs)
        print("Using modern Adafruit MCP3xxx library")
    except Exception as e:
        print(f"Error initializing modern library: {e}")
        MODERN_LIB = False

if not MODERN_LIB:
    # Legacy library initialization
    try:
        if SPI_TYPE == 'HW':
            # Use this for Hardware SPI
            mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(HW_SPI_PORT, HW_SPI_DEV))
        elif SPI_TYPE == 'SW':
            # Use this for Software SPI
            mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        print("Using legacy Adafruit_MCP3008 library")
    except Exception as e:
        print(f"Error initializing legacy library: {e}")
        sys.exit(1)

# Check command line arguments
if len(sys.argv) <= 1:
    print("Usage: python3 MCP3008-example.py <Analog Port>")
    print("Analog Port: 0-7 for MCP3008 channels")
    sys.exit(1)
else:
    try:
        analogPort = int(sys.argv[1])
        if analogPort < 0 or analogPort > 7:
            print("Error: Analog port must be between 0 and 7")
            sys.exit(1)
    except ValueError:
        print("Error: Analog port must be a number between 0 and 7")
        sys.exit(1)

print(f'Reading MCP3008 values on channel: {analogPort}')
print('Press Ctrl-C to exit...')

try:
    if MODERN_LIB:
        # Modern library channel setup
        channel_map = {
            0: MCP.P0, 1: MCP.P1, 2: MCP.P2, 3: MCP.P3,
            4: MCP.P4, 5: MCP.P5, 6: MCP.P6, 7: MCP.P7
        }
        chan = AnalogIn(mcp, channel_map[analogPort])
    
    while True:
        if MODERN_LIB:
            # Read using modern library
            val = chan.value
            voltage = chan.voltage
            print(f'Raw Value: {val:5d} | Voltage: {voltage:.3f}V')
        else:
            # Read using legacy library
            val = mcp.read_adc(analogPort)
            # Calculate approximate voltage (3.3V reference, 10-bit ADC)
            voltage = (val * 3.3) / 1023
            print(f'Raw Value: {val:5d} | Voltage: {voltage:.3f}V')
        
        sleep(dly)
        
except KeyboardInterrupt:
    print("\nExiting program.")
except Exception as e:
    print(f"Error during reading: {e}")