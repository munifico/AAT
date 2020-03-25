
today = 0
sum1 = 0

for i, vol in enumerate(range(10)):
    if i == 0:
        today = vol
        print(today)
    elif 0 <= i <= 10:
        sum1 = sum1 + vol
        print(sum1)