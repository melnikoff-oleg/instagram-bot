boy = ['roma', 'roman', 'stepan', 'tima', 'timofey', 'yaroslav', 'ben', 'alex', 'alexander', 'andrew', 'artem', 
'daniil', 'dan', 'denis', 'dmitry', 'dimas', 'egor', 'ilya', 'kirill', 'max', 'maks', 'maksim', 'mark', 
'mihail', 'michael', 'misha', 'mike', 'oleg', 'off', 'anton', 'tony', 'aleks', 'fedor', 'fedya', 'nikita', 
'nikolay', 'arseniy', 'danil', 'mikhail', 'igor', 'vlad', 'vladislav', 'vlados', 'sergey', 'sergo', 'alexandr', 
'anatoly', 'andrey', 'ignat', 'bodya', 'george', 'vladimir', 'vova', 'vovan', 'nazar', 'kolya', 'kolyan', 
'seva', 'pasha', 'kostya', 'konstantin', 'slava', 'gleb', 'valery', 'ivan', 'vanya', 'daniel', 'nik',
'tolya', 'tima', 'boris', 'borya', 'sava', 'kiril', 'aleksnader', 'albert', 
'anatoly', 'ars', 'artur', 'arthur', 'afonya', 'bogdan', 'vadim', 'valera', 'vitaly', 'vyacheslav', 
'gena', 'gennady', 'pavel', 'german', 'grisha', 'gregory', 'eugene', 'ilysha', 'kostik', 
'lev', 'leonid', 'makar', 'matvei', 'mathew', 'nick', 'nikola', 'petr', 'petya', 
'ruslan', 'serg', 'stanislav', 'stas', 'filipp', 'yury', 'yura', 'andr', 'ov', 'ev', 'paul', 'skiy', 'phil', 
'dima', 'dimka', 'mr', 'matvey', 'of', 'azat', 'yasha', 'in', 'slavik', 'sanek', 'richard', 'tema', 'vitya', 
'vano', 'evgeny', 'miroslav', 'yurka', 'yuriy', 'yurij', 'mitya', 'ildar', 'valentin', 'yra', 'volodya', 'rustam', 
'rodion', 'yung', 'lil', 'dmtry', 'joseph', 'iskander', 'gosha', 'daddy', 'graf', 'miguel', 'boy', 'timka', 
'zahar', 'zakhar', 'mahmud', 'sanya', 'danya', 'vania', 'renat']
 
girl = ['lyba', 'ritka', 'katusha', 'olesia', 'olesya', 'evgenia', 'veronica', 'mary', 'valia', 'appolinaria', 
'anastasia', 'helen', 'vasilisa', 'elena', 'lena', 'lenka', 'julia', 'jenia', 'kristina', 'kris', 'veleria', 
'elina', 'alina', 'angelina', 'varya', 'nadya', 'vlada', 'anfisa', 'olga', 'olya', 'kseny', 'ksenya', 'xenia', 
'xenya', 'ksusha', 'ksu', 'lena', 'natasha', 'natali', 'polly', 'polina', 'polinka', 'sofia', 'sofya', 
'valeria', 'tanya', 'tatiana', 'anya', 'taissia', 'ulyana', 'nastia', 'alena', 'alenka', 'eva', 'katya', 
'ekaterina', 'catharine', 'kate', 'elizaveta', 'liza', 'elisaveta', 'lisa', 'kira', 'rita', 'margo', 'maria', 
'masha', 'mashka', 'sofia', 'sonya', 'alexandra ', 'alisa', 'alice ', 'nastya', 'anastasia', 'anna', 'ann', 
'arina', 'valeria', 'lera', 'varvara', 'veronica', 'veronika', 'vera', 'victoria', 'viktoria', 'vika', 'darya', 
'dasha', 'daria', 'lidia', 'lida', 'maya', 'aleksandra', 'ova', 'eva', 'valentina', 'irina', 'ira', 'karina', 
'lara', 'larisa', 'marina', 'nina', 'oksana', 'sveta', 'svetlana', 'skaya', 'mrs', 'ina', 'girl', 'yulya', 
'mariya', 'asya', 'alla', 'sonia', 'lena', 'tania', 'sya', 'ochka', 'princess', 'ovna',
'yana', 'luba', 'shka', 'valya', 'jessica', 'lilia', 'marija', 'marie', 'stasya', 'polisha', 'katrin', 
'margarit', 'chka', 'yulia', 'nast', 'marusya', 'nika', 'olechka', 'eliz', 'elis', 'baby']
 
not_human = ['club', 'hse', 'gsom', 'spbu', 'itmo', 'boutique', 'sziu', 'unecon', 'shop']
 
def real_person(name):
    cropped = ''
    lst = 'ц'
    for i in name:
        if i != lst and i != '.' and i != '_':
            cropped += i
        lst = i
    name = cropped
    n = len(name)
    for i in range(n, 1, -1):
        for j in range(0, n - i + 1):
            s = name[j : j + i]
            if s in not_human:
                return False
    return True
 
def isGirl(name):
    if not real_person(name):
        return False
    cropped = ''
    lst = 'ц'
    for i in name:
        if i != lst and i != '.' and i != '_':
            cropped += i
        lst = i
    name = cropped
    n = len(name)
    ok = False
    for i in range(n, 1, -1):
        if ok:
            break
        for j in range(0, n - i + 1):
            s = name[j : j + i]
            if s in boy:
                return False
            if s in girl:
                return True
    return False
 
def isBoy(name):
    if not real_person(name):
        return False
    cropped = ''
    lst = 'ц'
    for i in name:
        if i != lst and i != '.' and i != '_':
            cropped += i
        lst = i
    name = cropped
    n = len(name)
    ok = False
    for i in range(n, 1, -1):
        if ok:
            break
        for j in range(0, n - i + 1):
            s = name[j : j + i]
            if s in boy:
                return True
            if s in girl:
                return False
    return False
 
def check(username, type):
    if type == 0:
        return isGirl(username)
    if type == 1:
        return isBoy(username)
    return real_person(username)