from PIL import ImageFont
import numpy as np
from fontTools.ttLib import TTFont

def fontsize2pixel(font_size, font_path, charset):
    font = ImageFont.truetype(font_path, size=font_size, index=0, encoding="utf-8")
    mask=font.getmask(charset)
    mask = np.array(mask).reshape(mask.size[1],mask.size[0]).astype(np.uint8)
    h,w=mask.shape[:2]

    return h

def is_font_support_charset(font_path, index, charset):
    """
    cannot detect some fonts because of the font designer; so first run this and next check by eye
    """
    # 1. determine by font config
    ttf = TTFont(font_path, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=index)
    chars = []
    # get all supported unicode points
    for x in ttf["cmap"].tables:
        for y in x.cmap.items():
            chars.append(y[0])
    chars = sorted(set(chars))

    charset = sorted([ord(c) for c in charset])
    for char in charset:
        if char not in chars:
            return False
    # 1. determine by font config

    # 2. determine by the mask of font. if mask is all zero means cannot see the char
    font = ImageFont.truetype(font_path, size=30, index=index, encoding="utf-8")
    for char in charset:
        mask = font.getmask(chr(char))
        mask = np.array(mask).reshape(mask.size[1],mask.size[0]).astype(np.uint8)
        if mask.size > 0 and mask.max()==255:
            return True
        else:
            return False
    # 2. determine by the mask of font. if mask is all zero means cannot see the char

    return True
