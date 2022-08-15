XmRED_LUMINOSITY = 0.30
XmGREEN_LUMINOSITY = 0.59
XmBLUE_LUMINOSITY = 0.11
XmINTENSITY_FACTOR = 75
XmLIGHT_FACTOR = 0
XmLUMINOSITY_FACTOR = 25

import sys

class Variations:
    def __init__(self, c):
        self.fg = c.copy()
        self.sel = c.copy()
        self.bs = c.copy()
        self.ts = c.copy()

        self.bg = c
        br, a, b = c.cielab()
        if br > 75:
            self.fg.srgb(0, 0, 0)
        else:
            self.fg.srgb(255, 255, 255)

        self.sel.cielab(L = br*0.8)
        self.bs.cielab(L = br*0.6, a = a * 0.7, b = b * 0.6)
        self.ts.cielab(L = 100 - (100-br)*0.3, a = a * 0.5, b = b * 0.4)

def Brightness(color):
    intensity = (color.r + color.g + color.b) / 3
    luminosity = (XmRED_LUMINOSITY * color.r + XmGREEN_LUMINOSITY * color.g + XmBLUE_LUMINOSITY * color.b)
    maxprimary = max(color.r, color.g, color.b)
    minprimary = min(color.r, color.g, color.b)
    light = (minprimary + maxprimary) / 2
    brightness = ((intensity * XmINTENSITY_FACTOR) + (light * XmLIGHT_FACTOR) + (luminosity * XmLUMINOSITY_FACTOR)) / 100

    return brightness

def CalculateColorsForLightBackground(bg):
    brightness = Brightness(bg) 
    return None
