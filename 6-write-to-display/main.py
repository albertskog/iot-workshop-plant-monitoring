from machine import Pin
from machine import I2C
from ssd1306 import SSD1306_I2C
from time import sleep

# The display driver is based on the FrameBuf library and supports the same methods:
# https://docs.micropython.org/en/latest/library/framebuf.html?highlight=framebuf#module-framebuf

i2c = I2C(scl=Pin(22), sda=Pin(21))
display = SSD1306_I2C(128, 64, i2c)

black = 0
white = 1

while True:
    # Clear the screen
    display.fill(black)

    # Text
    x_position = 10
    y_position = 10
    display.text("Test", x_position, y_position)

    # Horisontal line
    x_start = 0
    y_start = 20
    width = display.width
    display.hline(x_start, y_start, width, white)

    # Line
    x_start = 70
    y_start = 60
    x_end = 120
    y_end = 40
    display.line(x_start, y_start, x_end, y_end, white)

    # Individual pixel
    x_position = int(display.width / 2)
    y_position = int(display.height / 2)
    display.pixel(x_position, y_position, white)

    # Rectangle
    x_start = 10
    y_start = 40
    width = 20
    height = 20
    display.rect(x_start, y_start, width, height, white)

    # Filled rectangle
    x_start = 40
    y_start = 40
    width = 20
    height = 20
    display.fill_rect(x_start, y_start, width, height, white)

    # Show everything on the display
    display.show()

    sleep(1)

    # Countdown
    for i in range(5):
        x_position = int(display.width / 2) + 10 * i
        y_position = 10
        display.text(str(5 - i), x_position, y_position)
        display.show()
        sleep(1)

    # Scroll
    x_scroll = 1
    y_scroll = 0
    for i in range(display.width):
        display.scroll(x_scroll, y_scroll)
        display.show()

    sleep(1)
    display.fill(0)
    display.show()
    sleep(1)
