# Based on # https://github.com/blaz-r/pi_pico_neopixel/blob/main/neopixel.py
import neopixel	
import machine
import time

```
This is currently designed to work with WS2812B leds as far as i can tell
to get this working with other strips you just need to change the colour order ("GRB") in init

# Usage
import machine
numLeds = 300
ledPin = machine.Pin(0)
controller = Controller(numLeds,ledPin)
controller.fill(Colour.RED)
```

class Colour:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0) # Same as off


## Main Class
class Controller:
    def __init__(self,numLeds:int,ledPin,brightness:int=50):
        self.numLeds= numLeds
        self.brightness= brightness
        
        ## WS2812B has GRB Colour order change this according to yours
        self.strip = neopixel.Neopixel(num_leds=self.numLeds,pin=ledPin,mode="GRB", state_machine=0) ## Not exactly sure what state machine is for
        self.strip.brightness(brightness)
        
    def colourChase(self,color:Colour):
        for i in range(self.numLeds):
            self.strip[i] = color
            time.sleep(0.1)
            self.strip.show()

    def fill(self,colour:Colour):
        self.strip.fill(colour)
