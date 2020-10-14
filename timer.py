def timer():
    time = input().split(':')
    x = int(time[0])
    y = int(time[1])
    text = 'Поставьте будильник на любое из этих времен: '


    for i in range(6):
        if y == str(y):
            y = '' + y[-1]
            y = int(y)
        x -= 1.5

        if x % 1 != 0:
            x -= 0.5
            y += 30
            if y >= 60:
                y -= 60
                x += 1
        if x < 0:
            x = 24 + x

        if y <= 9:
            y = '0' + str(y)

        sleep = str(int(x)) + ':' + str(y)
        if i < 5:
            text = text + sleep + '; '
        else:
            text = text + sleep
    print(text)

timer()