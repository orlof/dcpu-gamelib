from subprocess import call
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]

onlyfiles.sort()

for f in onlyfiles:
    call(["convert", f, "-resize 64x48!", "-dither none", "-colors 16", "output/%s" % (f,)])

