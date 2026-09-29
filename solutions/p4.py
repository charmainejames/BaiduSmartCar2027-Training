import sys

params = []

for line in sys.stdin:

    text = line.strip()

    if not text or text.startswith("#"):
        continue

    key, value = text.split("=", 1)

    params.append((key, value))

params.sort(key=lambda item: item[0])#lambda...等价于一个简短函数，用于取第一个元素

for key, value in params:

    print(f"{key}: {value}")
