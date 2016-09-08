#!/usr/bin/env bash

# this is only an example
# edit crop area

convert $1 -crop 128x96+65+110 -resize 64x48! -dither none -colors 16 $2
