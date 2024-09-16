import time
import board
import neopixel_spi as neopixel

NUM_LEDS = 60
COLOR_ORDER = neopixel.GRB
DELAY = 0.1

spi = board.SPI()

pixels = neopixel.NeoPixel_SPI(spi, NUM_LEDS, pixel_order=COLOR_ORDER, auto_write=False)
pixels.fill(0x000000)
pixels.show()

print("Welcome to the LED Strip Test")

while True:
    i = int(input("Please enter which LED you would like to change it's color (or input 0 to clear all): "))
    if(i > 0 and i < 61):
        print(f"Please choose the number of the color you would like to change LED #{i} to")
        print("1. Red")
        print("2. Green")
        print("3. Blue")
        print("4. White")
        print("5. Yellow")
        print("6. Magenta")
        print("7. Cyan")
        print("8. Clear")
        color = int(input("Option: "))
    #Invalid LED
    if(i < 0 or i > 60):
        print("INVALID RANGE")
    #Clear All
    elif(i == 0):
        pixels.fill(0)
        pixels.show()
        print("CLEARING ALL")
    #Red
    elif(color == 1):
        print(f"Displaying LED #{i} as Red")
        pixels[i] = 0xFF0000
        pixels.show()
    #Green
    elif(color == 2):
        print(f"Displaying LED #{i} as Green")
        pixels[i] = 0x00FF00
        pixels.show()
    #Blue
    elif(color == 3):
        print(f"Displaying LED #{i} as Blue")
        pixels[i] = 0x0000FF
        pixels.show()
    #White
    elif(color == 4):
        print(f"Displaying LED #{i} as White")
        pixels[i] = 0xFFFFFF
        pixels.show()
    #Yellow
    elif(color == 5):
        print(f"Displaying LED #{i} as Yellow")
        pixels[i] = 0xFFFF00
        pixels.show()
    #Magenta
    elif(color == 6):
        print(f"Displaying LED #{i} as Magenta")
        pixels[i] = 0xFF00FF
        pixels.show()
    #Cyan
    elif(color == 7):
        print(f"Displaying LED #{i} as Cyan")
        pixels[i] = 0x00FFFF
        pixels.show()
    #Clear
    elif(color == 8):
        print(f"Clearing LED #{i}")
        pixels[i] = 0x000000
        pixels.show()
    #Invalid Color
    else:
        print("Invalid Color Option")