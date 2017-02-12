#!/usr/bin/python

import sys
from PIL import Image
from os import listdir
from os.path import isfile, isdir, join

dasm_prologue = """
;----------------------------------------------------------------
:show_image
;----------------------------------------------------------------
    hwn i
:detect_hardware__loop
    sub i, 1
    hwq i
    ifn a, 0xf615
        set pc, detect_hardware__loop
    ifn b, 0x7349
        set pc, detect_hardware__loop

    set a, 1
    set b, fontram
    hwi i

    set a, 2
    set b, fontram + 256
    hwi i

    set a, 0
    set b, fontram + 256 + 16
    hwi i

    set pc, pop

"""


def to_hex(word):
    return "0x" + format(ord(word[0]) << 8 | ord(word[1]), '04x')


class PixieImage(object):
    def __init__(self, filename):
        im = Image.open(filename)
        self.im = im.convert('RGB')
        self.rgb2idx = {}
        self.idx2rgb = {}

    def get_pixel(self, x, y):
        return tuple(map(lambda ctx: ctx >> 4, self.im.getpixel((x, y))))

    def set_pixel(self, x, y, rgb):
        self.im.putpixel((x, y), tuple(map(lambda ctx: ctx << 4, rgb)))

    def dasm_palette(self):
        for x in xrange(0, 128):
            for y in xrange(0, 96):
                pixel = self.get_pixel(x, y)
                self.set_pixel(x, y, pixel)
                if pixel not in self.rgb2idx:
                    idx = len(self.rgb2idx)
                    self.rgb2idx[pixel] = idx
                    self.idx2rgb[idx] = pixel

        dasm = ":palette\n"

        colors = sorted(self.rgb2idx, key=self.rgb2idx.get)
        while len(colors) < 16:
            colors.append((0, 0, 0))
        for idx, c in enumerate(colors):
            if idx % 8 == 0:
                dasm += "    DAT "
            dasm += "{0:#0{1}x}".format((c[0] << 8) | (c[1] << 4) | (c[2]), 6)
            if idx % 8 == 7:
                dasm += "\n"
            else:
                dasm += ", "

        return dasm

    def dasm_bitplanes(self):
        bp = [[], [], [], []]
        for y in xrange(0, 96):
            for x in xrange(0, 128):
                bg_rgb = self.get_pixel(x, y)
                bg_idx = self.rgb2idx[bg_rgb]

                if x % 16 == 0:
                    bp[0] += [0]
                    bp[1] += [0]
                    bp[2] += [0]
                    bp[3] += [0]

                bp[0][-1] <<= 1
                bp[0][-1] |= 1 if bg_idx & 1 == 1 else 0

                bp[1][-1] <<= 1
                bp[1][-1] |= 1 if bg_idx & 2 == 2 else 0

                bp[2][-1] <<= 1
                bp[2][-1] |= 1 if bg_idx & 4 == 4 else 0

                bp[3][-1] <<= 1
                bp[3][-1] |= 1 if bg_idx & 8 == 8 else 0

        dasm = ""
        for pidx, plane in enumerate(bp):
            dasm += ":bitplane%i\n" % pidx
            for idx, word in enumerate(plane):
                if idx % 8 == 0:
                    dasm += "    DAT "
                dasm += "{0:#0{1}x}".format(word, 6)
                if idx % 8 == 7:
                    dasm += "\n"
                else:
                    dasm += ", "

        return dasm


def process(fname):
    im = PixieImage("images/mp_pixie2.png")
    print im.dasm_palette()
    print im.dasm_bitplanes()


def main():
    import os
    print os.getcwd()

    process(sys.argv[1])

    #with open(sys.argv[-1][:-4] + ".dasm16", 'wb') as f:
    #    f.write(dasm)

    return 0


if __name__ == "__main__":
    sys.exit(main())
