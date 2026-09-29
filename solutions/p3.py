import sys

lines = 0
words = 0
chars = 0

for line in sys.stdin:

    text = line.rstrip("\r\n")

    lines += 1

    words += len(text.split())

    chars += len(text)

print(f"lines={lines} words={words} chars={chars}")
