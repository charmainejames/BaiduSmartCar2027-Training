levels = list(map(int, input().split()))

low = 0
ok = 0
full = 0

for index, level in enumerate(levels, start=1):
    if level < 30:
        category = "low"
        low += 1

    elif level <= 70:
        category = "ok"
        ok += 1

    else:
        category = "full"
        full += 1

    print(f"tower_{index}: {category}")

print(f"low={low} ok={ok} full={full}")
