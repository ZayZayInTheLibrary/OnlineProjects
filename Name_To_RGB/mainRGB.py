from functools import reduce

name = input("What is your name?\n")

nameAscii = [ord(c) for c in name]
nameAscii = list(map(int, nameAscii))
nameAsciiSum = sum(nameAscii)
nameAsciiDif = reduce(lambda x, y: x - y, nameAscii)
nameAsciiMult = reduce(lambda x, y: x * y, nameAscii)
nameAsciiSum = nameAsciiSum % 256
nameAsciiDif = nameAsciiDif % 256
nameAsciiMult = nameAsciiMult % 256

print(f"RGB: {nameAsciiSum, nameAsciiDif, nameAsciiMult}")

def textToRGB(text):
    name = text
    nameAscii = [ord(c) for c in name]
    nameAscii = list(map(int, nameAscii))
    nameAsciiSum = sum(nameAscii)
    nameAsciiDif = reduce(lambda x, y: x - y, nameAscii)
    nameAsciiMult = reduce(lambda x, y: x * y, nameAscii)
    nameAsciiSum = nameAsciiSum % 256
    nameAsciiDif = nameAsciiDif % 256
    nameAsciiMult = nameAsciiMult % 256
    return (nameAsciiSum, nameAsciiDif, nameAsciiMult)