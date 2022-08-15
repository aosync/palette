import palette
import motif
import sys

with open(sys.argv[1]) as file:
    PAL = palette.palette(file)

def genset(num, id):
    v = motif.Variations(PAL[id])
    print("Colorset %d fg %s, bg %s, hi %s, sh %s, Plain, NoShape" % (num, v.fg.dump_srgb(), v.bg.dump_srgb(), v.ts.dump_srgb(), v.bs.dump_srgb()))

genset(0, 1)
genset(1, 1)
genset(2, 0)

genset(3, 1)
genset(4, 0)

genset(5, 4)
genset(6, 4)
genset(7, 4)
genset(8, 4)

genset(10, 4)
