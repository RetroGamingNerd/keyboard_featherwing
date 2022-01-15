from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
import adafruit_ili9341
import displayio
import digitalio
import tsc2004
import time
import adafruit_mcp9808
import neopixel
import board

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

i2c = board.I2C()

touch = tsc2004.TSC2004(i2c)
while not touch.touched:
    pass

print(touch.read_data())

neopix_pin = board.D11
pixels = neopixel.NeoPixel(neopix_pin, 1,brightness=0.1)
pixels[0] = 0xFF00FF

i2c = board.I2C()
kbd = BBQ10Keyboard(i2c)
mcp = adafruit_mcp9808.MCP9808(i2c)


message= ""

i = 1
while True:
    if kbd.key_count > 1:
        keys = kbd.keys
        state,key=keys[1]
        print(key,end='')
        if key != '\n':
            message+=key
        else:
            print(message)
            if message == "import temp":
                print("Printing Temperature Readings")
                tempC = mcp.temperature
                tempF = tempC * 9 / 5 + 32
                print("Temperature: {} C {} F ".format(tempC, tempF))
                time.sleep(2)
            elif message == "do that":
                print("got that")
            message= ""

