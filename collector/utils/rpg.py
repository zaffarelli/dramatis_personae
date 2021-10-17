
import os


def roll(maxi):
    """ A more random '1 to maxi' dice roller  """
    randbyte = int.from_bytes(os.urandom(1), byteorder='big', signed=False)
    x = int(randbyte / 256 * (maxi)) + 1
    return x


def d(number, faces):
    total = 0
    for x in range(number):
        total += roll(faces)
    return total


def smart_code(str):
    return str.replace(' ','').replace(')','').replace('(','_').replace('é','e').replace('&','et').replace('ç','c').replace('è','e').replace('ê','e').replace('"','').replace("'",'').replace('à','a').replace('â','a').replace('-','').lower()