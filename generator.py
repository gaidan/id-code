import zlib
import string
import random
from PIL import Image, ImageDraw

# LIST OF CHARACTERS USEABLE IN USER PRIVATE CODE
CHARACTERS = string.printable[0:len(string.printable)-6]

# GENERATE 8 STRING PRIVATE CODE
def generate_code() -> str:
    return ''.join([random.choice(CHARACTERS) for i in range(0, 8)])

# CREATE PUBLIC CODE (HEX ADLER32 HASH OF PRIVATE CODE)
def generate_public_code(input_code: str) -> str:
    return str(hex(zlib.adler32(input_code.encode())))[2:10]

# CONVERT CODE TO BINARY
def code_to_binary(input_code: str) -> list:
    return [bin(ord(char)) for char in input_code]

# FORMAT BINARY SO IT IS 8 CHARACTERS LONG
def format_binary(input_list: list) -> list:
    input_list = [i[2:len(i)] for i in input_list]
    output = []
    for num in input_list:
        n = list(num)
        for i in range(0, (8-len(num))):
            n.insert(0, '0')
        n = ''.join(n)
        output.append(n)
    return output

code = generate_code()
public_code = generate_public_code(code)
print("PRIVATE ID > {}".format(code))
print("PUBLIC ID > {}".format(public_code))

code = code_to_binary(code)
public_code = code_to_binary(public_code)

code = format_binary(code)
public_code = format_binary(public_code)

# CREATE IMAGE PIXEL DATA FROM BINARY CONVERSION OF CODES
pil_data_private = []
pil_data_public = []
for num in code:
    for char in num:
        if char == '0':
            pil_data_private.append((255, 255, 255))
        else:
            pil_data_private.append((0, 0, 0))
for num in public_code:
    for char in num:
        if char == '0':
            pil_data_public.append((255, 255, 255))
        else:
            pil_data_public.append((0, 0, 0))

bckg = Image.new("RGB", (900, 900), (0, 0, 255))
im = Image.new('RGB', (8, 8))
im_p = Image.new('RGB', (8, 8))
im.putdata(pil_data_private)
im_p.putdata(pil_data_public)
im = im.resize((800, 800), 0)
im_p = im_p.resize((800, 800), 0)
bckg.paste(im, (50, 50))
draw = ImageDraw.Draw(bckg)
draw.rectangle((0, 0, 50, 50), fill=(255, 0, 0))
draw.rectangle((850, 850, 900, 900), fill=(0, 255, 0))
draw.rectangle((850, 0, 900, 50), fill=(255, 255, 0))
draw.rectangle((0, 850, 50, 900), fill=(255, 0, 255))
bckg.save('private.png')
bckg = Image.new("RGB", (900, 900), (0, 0, 255))
bckg.paste(im_p, (50, 50))
draw = ImageDraw.Draw(bckg)
draw.rectangle((0, 0, 50, 50), fill=(255, 0, 0))
draw.rectangle((850, 850, 900, 900), fill=(0, 255, 0))
draw.rectangle((850, 0, 900, 50), fill=(255, 255, 0))
draw.rectangle((0, 850, 50, 900), fill=(255, 0, 255))
bckg.save('public.png')
