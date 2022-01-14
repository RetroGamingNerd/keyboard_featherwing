from bbq10keyboard import BBQ10Keyboard
import adafruit_ili9341
import displayio
import digitalio
import tsc2004
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

i2c = board.I2C()
kbd = BBQ10Keyboard(i2c)

while kbd.key_count == 0:
    pass

print(kbd.keys)
