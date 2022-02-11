from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
import adafruit_ili9341
import displayio
import digitalio
import tsc2004
import time
from adafruit_lc709203f import LC709203F
import adafruit_mcp9808
import neopixel
import microcontroller
import board
import gc

neopix_pin = board.D11
pixels = neopixel.NeoPixel(neopix_pin, 1,brightness=0.05)
pixels[0] = 0x00FF00

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

gc.collect()
start_mem = gc.mem_free()
print( "Memory: {} bytes".format(start_mem) )

i2c = board.I2C()
kbd = BBQ10Keyboard(i2c)
sensor = LC709203F(board.I2C())
try:
    mcp = adafruit_mcp9808.MCP9808(i2c)
    print ('MCP9808 Connected')
except:
    print ('MCP9808 Disconnected')
    pass

time.sleep(1)

print(1 * "\n")
print("     _|    _|            _|  _|")
print("     _|    _|    _|_|    _|  _|    _|_|")
print("     _|_|_|_|  _|_|_|_|  _|  _|  _|    _|")
print("     _|    _|  _|        _|  _|  _|    _|")
print("     _|    _|    _|_|_|  _|  _|    _|_|")
print(1 * "\n")
print("------------- Touch Screen to Start -------------")

touch = tsc2004.TSC2004(i2c)
while not touch.touched:
    pass

print(touch.read_data())
print(2 * "\n")
print("---------------------- MENU ----------------------")
print(" ******* Connect Sensors Before Selecting ******* ")
print()
print("1# Enter 'check temp' for temperature data")
print()
print("2# Enter 'check battery' for battery level")
print()
print("3# Enter 'test' for test reply")
print()
print("4# Enter 'info' for microcontroller information")
print()
print("5# Enter 'menu' for MENU")
print()

message= ""

while True:
    if kbd.key_count > 1:
        keys = kbd.keys
        state,key=keys[1]
        print(key,end='')
        if key != '\n':
            message+=key
        else:
            if message == "check temp":
                for i in range(30):
                    print()
                    print("Reading", i+1)
                    tempC = mcp.temperature
                    tempF = tempC * 9 / 5 + 32
                    print("Temperature: {} C {} F ".format(tempC, tempF))
                    time.sleep(2)
                print()
                print("Finished!")
            elif message == "check battery":
                print(7 * "\n")
                print("Printing Battery Readings")
                print("Make sure battery is plugged into the board!")
                print()
                print("IC version:", hex(sensor.ic_version))
                print()
                print("Battery: %0.3f Volts / %0.1f %%" % (sensor.cell_voltage, sensor.cell_percent))
                time.sleep(1)
            elif message == "info":
                gc.collect()
                end_mem = gc.mem_free()
                print(7 * "\n")
                print("CPU Information")
                print()
                print("Project: Portable Sensor Platform")
                print("OS Version 1.3")
                print()
                print("CPU 1 Temperature:", microcontroller.cpus[0].temperature)
                print("CPU 1 Frequency:", microcontroller.cpus[0].frequency)
                print()
                print("CPU 2 Temperature:", microcontroller.cpus[1].temperature)
                print("CPU 2 Frequency:", microcontroller.cpus[1].frequency)
                print()
                print( "Available Memory: {} bytes".format(end_mem) )
                print( "Memory Used: {} bytes".format(start_mem - end_mem) )
            elif message == "test 1":
                print("test 1 reply")
            elif message == "menu":
                print(1 * "\n")
                print("---------------------- MENU ----------------------")
                print(" ********** Choose from the list below ********** ")
                print()
                print("1# Enter 'check temp' for temperature data")
                print()
                print("2# Enter 'check battery' for battery level")
                print()
                print("3# Enter 'test' for test reply")
                print()
                print("4# Enter 'info' for microcontroller information")
                print()
                print("5# Enter 'menu' for MENU")
                print()
            message= ""
