#
# j00zek: this file has changed name just to avoid errors using opkg (situation when file was installed by different pockage)
# and make it available for images whic doesn't have it e.g. VTI
#
# Converts hex colors to formatted strings,
# suitable for embedding in python code.
#
# hex:
# 0 1 2 3 4 5 6 7 8 9 a b c d e f
# converts to:
# 0 1 2 3 4 5 6 7 8 9 : ; < = > ?

def Hex2strColor(rgb):
  out = ""
  for i in range(28, -1, -4):
    out += "%s" % chr(0x30 + (rgb >> i & 0x0F))
  return "\c%s" % out
