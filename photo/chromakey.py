#!/usr/bin/python
from PIL import Image
from pprint import pprint
import copy
import numpy
import sys
import math

def colorclose(Cb_p, Cr_p):
  Cb_key = 92
  Cr_key = 86
  tola = 44.0
  tolb = 52.0
  cb2 = (Cb_key-Cb_p) * (Cb_key-Cb_p)
  cr2 = (Cr_key-Cr_p) * (Cr_key-Cr_p)
  temp = math.sqrt(cb2+cr2)

  if temp < tola:
    return True
  elif (temp < tolb):
    return (temp-tola)/(tolb-tola)
  else:
    return False

def chromakey(fg, bg):

  fg_rgb = numpy.array(fg)
  fg_ycbcr = fg.convert("YCbCr")
  fg_ycbcr = numpy.ndarray((fg.size[1], fg.size[0], 3), 'u1', fg_ycbcr.tostring())

  bg_rgb = numpy.array(bg)

  xsize = len(fg_rgb)
  ysize = len(fg_rgb[0])
  out = numpy.zeros((xsize,ysize,3))
  out = out.astype('uint8')

  irange = range(0,xsize)
  jrange = range(0,ysize)
  krange = range(0,3)

  for i in irange:
    for j in jrange:
      Cb_p = int(fg_ycbcr[i][j][1])
      Cb_r = int(fg_ycbcr[i][j][2])

      mask = 1-colorclose(Cb_p, Cb_r)

      if mask == True:
        out[i][j] = fg_rgb[i][j]
      elif mask == False:
        out[i][j] = bg_rgb[i][j]
      else:
        maskarray = [mask, mask, mask]
        out[i][j] = fg_rgb[i][j] - (mask * fg_rgb[i][j]) + (bg_rgb[i][j] * mask)

  return Image.fromarray(out, "RGB")