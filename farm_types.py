import gender

def check(i, cur, x, y):
    if x > 2000 or y < 100:
        return False
    if i == 0:
        return x / y < 20 and y < 800 and y / x < 2 and x > 150 and y > 100
    if i == 1:
        return x > 200 and x / y > 1
    if i == 2:
        return x > 250 and x / y > 1.1
    if i == 3: 
        return x > 300 and x / y > 1.1
    if i == 4:
        return x > 350 and x / y > 1.1
    if i == 5:
        return x > 400 and x / y > 1.1
    if i == 6:
        return x > 450 and x / y > 1.1
    if i == 7:
        return x > 500 and x / y > 1.1
    if i == 8:
        return x > 500 and x / y > 1.2
    if i == 9:
        return x > 550 and x / y > 1.2
    if i == 10:
        return x > 600 and x / y > 1.2
    if i == 11:
        return x > 650 and x / y > 1.2
    if i == 12:
        return x > 700 and x / y > 1.3
    if i == 13: #GROM
        return x > 250 and y < 500 and x / y > 1.1
    if i == 14: #FIMOSHA
        return x > 500 and y < 425