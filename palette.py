import os
import re
import sys
import motif

RGB8_TO_16 = 65535 / 255

def srgb_to_lin(C):
    C /= 255.0

    if C > 1.0:
        C = 1.0
    elif C < 0.0:
        C = 0.0

    THRESH = 0.04045

    if C <= THRESH:
        return C / 12.92
    else:
        return ((C + 0.055)/1.055)**(2.4)

def lin_to_srgb(C):
    # Check if in Gamut
    if C > 1.0:
        C = 1.0
    elif C < 0.0:
        C = 0.0

    THRESH = 0.0031308
    R = 0

    if C <= THRESH:
        R = 12.92 * C
    else:
        R = 1.055 * C**(1/2.4) - 0.055

    return R * 255.0

def xyz_to_lab(t):
    delta = 6/29
    if t > delta**3:
        return t**(1/3)
    else:
        return t/(3 * delta**2) + 4/29

def lab_to_xyz(t):
    delta = 6/29
    if t > delta:
        return t**3
    else:
        return 3 * delta**2 * (t - 4/29)

class Color:
    # The Color class holds a 48-bit color specification,
    # which is the one used in X BitMap files

    def __init__(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b
        self.lin_R = 0
        self.lin_G = 0
        self.lin_B = 0
        self.cie_X = 0
        self.cie_Y = 0
        self.cie_Z = 0
        self.cie_L = 0
        self.cie_a = 0
        self.cie_b = 0

        self.update_lin()

    def downgrade_srgb(self):
        self.R = lin_to_srgb(self.lin_R)
        self.G = lin_to_srgb(self.lin_G)
        self.B = lin_to_srgb(self.lin_B)
       

    def update_lin(self):
        self.lin_R = srgb_to_lin(self.R)
        self.lin_G = srgb_to_lin(self.G)
        self.lin_B = srgb_to_lin(self.B)
        self.update_cie_xyz()         

    def downgrade_lin(self):
        self.lin_R =  3.2406*self.cie_X     - 1.5372*self.cie_Y     - 0.4986*self.cie_Z
        self.lin_G = -0.9689*self.cie_X     + 1.8758*self.cie_Y     + 0.0415*self.cie_Z
        self.lin_B =  0.05569998*self.cie_X - 0.20399998*self.cie_Y + 1.0570*self.cie_Z
        self.downgrade_srgb()

    def update_cie_xyz(self):
        self.cie_X = 0.41239559*self.lin_R + 0.35758343*self.lin_G + 0.18049265*self.lin_B
        self.cie_Y = 0.21258623*self.lin_R + 0.7151703 *self.lin_G + 0.0722005 *self.lin_B
        self.cie_Z = 0.01929722*self.lin_R + 0.11918386*self.lin_G + 0.95049713*self.lin_B
        self.update_cie_lab()

    def downgrade_cie_xyz(self):
        self.cie_X = 0.950489*lab_to_xyz((self.cie_L + 16)/116 + self.cie_a / 500)
        self.cie_Y = lab_to_xyz((self.cie_L + 16)/116)
        self.cie_Z = 1.08884*lab_to_xyz((self.cie_L + 16)/116 - self.cie_b / 200)
        self.downgrade_lin()

    def update_cie_lab(self):
        self.cie_L = 116*xyz_to_lab(self.cie_Y) - 16
        self.cie_a = 500*(xyz_to_lab(self.cie_X / 0.950489) - xyz_to_lab(self.cie_Y))
        self.cie_b = 200*(xyz_to_lab(self.cie_Y) - xyz_to_lab(self.cie_Z / 1.08884)) 
   
    def srgb(self, R = None, G = None, B = None):
        if R != None:
            self.R = R
        if G != None:
            self.G = G
        if B != None:
            self.B = B

        if R != None or B != None or G != None:
            self.update_lin()
        
        return self.R, self.G, self.B

    def lin(self, R = None, G = None, B = None):
        if R != None:
            self.lin_R = R
        if G != None:
            self.lin_G = G
        if B != None:
            self.lin_B = B

        if R != None or B != None or G != None:
            self.downgrade_srgb()
            self.update_cie_xyz()

        return self.lin_R, self.lin_G, self.lin_G

    def ciexyz(self, X = None, Y = None, Z = None):
        if X != None:
            self.cie_X = X
        if Y != None:
            self.cie_Y = Y
        if Z != None:
            self.cie_Z = Z

        if X != None or Y != None or Z != None:
            self.downgrade_lin()
            self.update_cie_lab()

        return self.cie_X, self.cie_Y, self.cie_Z

    def cielab(self, L = None, a = None, b = None):
        if L != None:
            self.cie_L = L
        if a != None:
            self.cie_a = a
        if b != None:
            self.cie_b = b

        if L != None or a != None or b != None:
            self.downgrade_cie_xyz()
        
        return self.cie_L, self.cie_a, self.cie_b

    # Dumps the color in a string form
    def dump_srgb(self):
        R, G, B = self.srgb()
        R = int(R + 0.5)
        G = int(G + 0.5)
        B = int(B + 0.5)
        return "#%02x%02x%02x" % (R, G, B)

    def dump_rgb16(self):
        R, G, B = self.srgb()
        R = int(R * RGB8_TO_16 + 0.5)
        G = int(G * RGB8_TO_16 + 0.5)
        B = int(B * RGB8_TO_16 + 0.5)
        return "#%04x%04x%04x" % (R, G, B)

    # Parses a string containing the color into the color
    def parse_rgb16(string):
        # Skip the '#'
        string = string[1:]

        channels = re.match(r"([0-9A-Fa-f]{4})([0-9A-Fa-f]{4})([0-9A-Fa-f]{4})", string)
        r = int(channels.group(1), 16) / RGB8_TO_16
        g = int(channels.group(2), 16) / RGB8_TO_16
        b = int(channels.group(3), 16) / RGB8_TO_16

        return Color(r, g, b)

    def parse_srgb(string):
        string = string[1:]
        
        channels = re.match(r"([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})", string)
        R = int(channels.group(1), 16)
        G = int(channels.group(2), 16)
        B = int(channels.group(3), 16)

        return Color(R, G, B)

    def copy(self):
        return Color(self.R, self.G, self.B) 

def palette(file):
    return [Color.parse_rgb16(line) for line in file if line.startswith("#")] 

if __name__ == '__main__':
    f = open(sys.argv[1])
    p = palette(f)
    f.close()

    num = int(sys.argv[3]) - 1

    bg = motif.Variations(p[num])
    f = open(sys.argv[2], 'r')
    for line in f:
        line = re.sub('(s[\t ]+background[\t ]+m[\t ]+(black|white)[\t ]+c[\t ]+)(.*)', r'\1' + bg.bg.dump_rgb16() + '",', line)
        line = re.sub('(s[\t]+foreground[\t ]+m[\t ]+(black|white)[\t ]+c[\t ]+)(.*)', r'\1' + bg.fg.dump_rgb16() + '",', line)
        line = re.sub('(s[\t ]+topShadowColor[\t ]+m[\t ]+(black|white)[\t ]+c[\t ]+)(.*)', r'\1' + bg.ts.dump_rgb16() + '",', line)
        line = re.sub('(s[\t ]+bottomShadowColor[\t ]+m[\t ]+(black|white)[\t ]+c[\t ]+)(.*)', r'\1' + bg.bs.dump_rgb16() + '",', line)
        line = re.sub('(s[\t ]+selectColor[\t ]+m[\t ]+(black|white)[\t ]+c[\t ]+)(.*)', r'\1' + bg.sel.dump_rgb16() + '",', line)
        sys.stdout.write(line)
    f.close()
    sys.stdout.flush()    
