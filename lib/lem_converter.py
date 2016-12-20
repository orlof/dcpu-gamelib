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

:fontram
    dat 0x0000, 0x0000, 0x0000, 0xC0C0, 0x0000, 0x3030, 0x0000, 0xF0F0
    dat 0x0000, 0x0C0C, 0x0000, 0xCCCC, 0x0000, 0x3C3C, 0x0000, 0xFCFC
    dat 0x0000, 0x0303, 0x0000, 0xC3C3, 0x0000, 0x3333, 0x0000, 0xF3F3
    dat 0x0000, 0x0F0F, 0x0000, 0xCFCF, 0x0000, 0x3F3F, 0x0000, 0xFFFF
    dat 0xC0C0, 0x0000, 0xC0C0, 0xC0C0, 0xC0C0, 0x3030, 0xC0C0, 0xF0F0
    dat 0xC0C0, 0x0C0C, 0xC0C0, 0xCCCC, 0xC0C0, 0x3C3C, 0xC0C0, 0xFCFC
    dat 0xC0C0, 0x0303, 0xC0C0, 0xC3C3, 0xC0C0, 0x3333, 0xC0C0, 0xF3F3
    dat 0xC0C0, 0x0F0F, 0xC0C0, 0xCFCF, 0xC0C0, 0x3F3F, 0xC0C0, 0xFFFF
    dat 0x3030, 0x0000, 0x3030, 0xC0C0, 0x3030, 0x3030, 0x3030, 0xF0F0
    dat 0x3030, 0x0C0C, 0x3030, 0xCCCC, 0x3030, 0x3C3C, 0x3030, 0xFCFC
    dat 0x3030, 0x0303, 0x3030, 0xC3C3, 0x3030, 0x3333, 0x3030, 0xF3F3
    dat 0x3030, 0x0F0F, 0x3030, 0xCFCF, 0x3030, 0x3F3F, 0x3030, 0xFFFF
    dat 0xF0F0, 0x0000, 0xF0F0, 0xC0C0, 0xF0F0, 0x3030, 0xF0F0, 0xF0F0
    dat 0xF0F0, 0x0C0C, 0xF0F0, 0xCCCC, 0xF0F0, 0x3C3C, 0xF0F0, 0xFCFC
    dat 0xF0F0, 0x0303, 0xF0F0, 0xC3C3, 0xF0F0, 0x3333, 0xF0F0, 0xF3F3
    dat 0xF0F0, 0x0F0F, 0xF0F0, 0xCFCF, 0xF0F0, 0x3F3F, 0xF0F0, 0xFFFF
    dat 0x0C0C, 0x0000, 0x0C0C, 0xC0C0, 0x0C0C, 0x3030, 0x0C0C, 0xF0F0
    dat 0x0C0C, 0x0C0C, 0x0C0C, 0xCCCC, 0x0C0C, 0x3C3C, 0x0C0C, 0xFCFC
    dat 0x0C0C, 0x0303, 0x0C0C, 0xC3C3, 0x0C0C, 0x3333, 0x0C0C, 0xF3F3
    dat 0x0C0C, 0x0F0F, 0x0C0C, 0xCFCF, 0x0C0C, 0x3F3F, 0x0C0C, 0xFFFF
    dat 0xCCCC, 0x0000, 0xCCCC, 0xC0C0, 0xCCCC, 0x3030, 0xCCCC, 0xF0F0
    dat 0xCCCC, 0x0C0C, 0xCCCC, 0xCCCC, 0xCCCC, 0x3C3C, 0xCCCC, 0xFCFC
    dat 0xCCCC, 0x0303, 0xCCCC, 0xC3C3, 0xCCCC, 0x3333, 0xCCCC, 0xF3F3
    dat 0xCCCC, 0x0F0F, 0xCCCC, 0xCFCF, 0xCCCC, 0x3F3F, 0xCCCC, 0xFFFF
    dat 0x3C3C, 0x0000, 0x3C3C, 0xC0C0, 0x3C3C, 0x3030, 0x3C3C, 0xF0F0
    dat 0x3C3C, 0x0C0C, 0x3C3C, 0xCCCC, 0x3C3C, 0x3C3C, 0x3C3C, 0xFCFC
    dat 0x3C3C, 0x0303, 0x3C3C, 0xC3C3, 0x3C3C, 0x3333, 0x3C3C, 0xF3F3
    dat 0x3C3C, 0x0F0F, 0x3C3C, 0xCFCF, 0x3C3C, 0x3F3F, 0x3C3C, 0xFFFF
    dat 0xFCFC, 0x0000, 0xFCFC, 0xC0C0, 0xFCFC, 0x3030, 0xFCFC, 0xF0F0
    dat 0xFCFC, 0x0C0C, 0xFCFC, 0xCCCC, 0xFCFC, 0x3C3C, 0xFCFC, 0xFCFC
    dat 0xFCFC, 0x0303, 0xFCFC, 0xC3C3, 0xFCFC, 0x3333, 0xFCFC, 0xF3F3
    dat 0xFCFC, 0x0F0F, 0xFCFC, 0xCFCF, 0xFCFC, 0x3F3F, 0xFCFC, 0xFFFF

"""




def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2


def to_hex(word):
    return "0x" + format(ord(word[0]) << 8 | ord(word[1]), '04x')


class LEMImage(object):
    def __init__(self, filename):
        im = Image.open(filename)
        self.im = im.convert('RGB')
        self.rgb2idx = {}
        self.idx2rgb = {}

    def get_pixel(self, x, y):
        return tuple(map(lambda ctx: ctx >> 4, self.im.getpixel((x, y))))

    def set_pixel(self, x, y, rgb):
        self.im.putpixel((x, y), tuple(map(lambda ctx: ctx << 4, rgb)))

    def assign_color_indexes(self):
        for x in xrange(0, 64):
            for y in xrange(0, 48):
                pixel = self.get_pixel(x, y)
                self.set_pixel(x, y, pixel)
                if pixel not in self.rgb2idx:
                    idx = len(self.rgb2idx)
                    self.rgb2idx[pixel] = idx
                    self.idx2rgb[idx] = pixel

    def find_two_colors(self, points):
        best = (float('inf'), None, None)
        for pal1 in self.rgb2idx:
            for pal2 in self.rgb2idx:
                total_distance = 0
                for p in points:
                    d1 = distance_squared(pal1, p)
                    d2 = distance_squared(pal2, p)
                    total_distance += min(d1, d2)
                if total_distance < best[0]:
                    best = (total_distance, pal1, pal2)

        return best

    def reduce_cell_colors(self):
        # for each character position
        for x in xrange(0, 64, 2):
            for y in xrange(0, 48, 4):
                # find two optimal colors
                pixels = []
                for sx in xrange(x, x + 2):
                    for sy in xrange(y, y + 4):
                        pixels.append(self.get_pixel(sx, sy))

                best = self.find_two_colors(pixels)

                # change every pixel to one of the target colors
                for sx in xrange(x, x + 2):
                    for sy in xrange(y, y + 4):
                        rgb = self.get_pixel(sx, sy)
                        self.set_pixel(sx, sy,
                            best[1] if distance_squared(rgb, best[1]) < distance_squared(rgb, best[2]) else best[2])

    def sector(self):
        memory = []
        colors = sorted(self.rgb2idx, key=self.rgb2idx.get)
        while len(colors) < 16:
            colors.append((0, 0, 0))
        for idx, c in enumerate(colors):
            memory.append((c[0] << 8) | (c[1] << 4) | (c[2]))

        for y in xrange(0, 48, 4):
            for x in xrange(0, 64, 2):
                bg_rgb = self.get_pixel(x, y)
                bg_idx = self.rgb2idx[bg_rgb]

                fg = set()
                glyph = 0
                marker = 1
                for sx in xrange(x+1, x-1, -1):
                    for sy in xrange(y+3, y-1, -1):
                        rgb = self.get_pixel(sx, sy)
                        idx = self.rgb2idx[rgb]

                        fg.add(idx)

                        if idx != bg_idx:
                            glyph |= marker

                        marker <<= 1

                fg.remove(bg_idx)
                if len(fg) == 0:
                    fg_idx = bg_idx
                elif len(fg) == 1:
                    fg_idx = fg.pop()
                else:
                    print "ERROR: Too many colors in segment"
                    sys.exit()

                memory.append((fg_idx << 12) | (bg_idx << 8) | glyph)

        return ''.join(chr((x >> 8) & 0xFF) + chr(x & 0xFF) for x in memory)

    def convert(self):
        self.assign_color_indexes()
        self.reduce_cell_colors()
        return self.sector()

    def calculate_colors(self, im):
        colors = set()
        for c, g in zip(im[::2], im[1::2]):
            colors.add(self.idx2rgb[ord(c) & 4])
            if g != 0:
                colors.add(self.idx2rgb[ord(c) >> 4])
        return len(colors)


def pad(data):
    while len(data) % 1024 != 0:
        data += chr(0)
    return data


def calculate_glyphs(im):
    glyphs = set()
    for g in im[1::2]:
        glyphs.add(g)
    return len(glyphs)


data = ''
dasm = ''


def process_file(fname):
    global data, dasm

    im = LEMImage(fname)
    dasm += ":" + fname + "\n"
    image_data = im.convert()

    print "Filename: %s" % (fname,)
    print "Glyphs  : %s" % (calculate_glyphs(image_data[16:]))
    print "Colors  : %s" % (im.calculate_colors(image_data[16:]))

    data += pad(image_data)
    for idx, w in enumerate(xrange(0, len(image_data), 2)):
        if idx % 8 == 0:
            dasm += "    dat "
        else:
            dasm += ", "

        dasm += "0x" + format(ord(image_data[w]) << 8 | ord(image_data[w + 1]), '04x')

        if idx % 8 == 7:
            dasm += "\n"

    dasm += "\n"


def process(fname):
    if isdir(fname):
        for f in listdir(fname):
            process(join(fname, f))
    else:
        process_file(fname)


def main():
    global data, dasm

    for fname in sys.argv[1:-1]:
        process(fname)

    if len(sys.argv) == 2:
        dasm = dasm_prologue + dasm

    with open(sys.argv[-1], 'wb') as f:
        f.write(data)

    with open(sys.argv[-1][:-4] + ".dasm16", 'wb') as f:
        f.write(dasm)


if __name__ == "__main__":
    sys.exit(main())
