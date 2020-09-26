import bot
import time
from time import sleep
from random import randint
import random
import farm_types
import calc_bot
from user import *
import calc_bot
from constants import *

def multifarm_iteration(users, types, col):
    n = len(users)
    finished = []
    for i in range(n):
        finished.append(False)
        if not types[i]:
            users[i].get_bad_guys()
        print(str(len(users[i].temp_bad_guys) - users[i].temp_bad_guys_ind) + ' BAD GUYS FOUND ON ' + users[i].username)
    print('BAD GUYS CALCED, FARM STARTED')
    ig_bot = bot.InstagramBot('lol', 'lol')
    for i in range(col):
        for j in range(n):
            if finished[j]:
                continue
            ig_bot.username = users[j].username
            ig_bot.password = users[j].password
            ig_bot.login()
            sleep(2)
            for k in range(2):
                if types[j]:
                    while(users[j].farm_ind < users[j].ff_ind and not users[j].good_stats(users[j].farm_ind)):
                        users[j].farm_ind += 1
                    if users[j].farm_ind == users[j].ff_ind:
                        print("FF ENDED, FARM STOPPED ON " + users[j].username)
                        finished[j] = True
                    else:
                        ig_bot.natural_subscribe(users[j].most_common[users[j].farm_ind][0])
                        users[j].used.append(users[j].most_common[users[j].farm_ind][0])
                        users[j].add_new_used(users[j].farm_ind)
                        users[j].farm_ind += 1
                else:
                    if users[j].temp_bad_guys_ind == len(users[j].temp_bad_guys):
                        print("BAD GUYS ENDED, ANTIFARM STOPPED ON " + users[j].username)
                        finished[j] = True
                    else:
                        ig_bot.natural_unsubscribe(users[j].temp_bad_guys[users[j].temp_bad_guys_ind])
                        users[j].temp_bad_guys_ind += 1
            ig_bot.exit()
            if i < col - 1 or j < n - 1:
                secs = 10
                print("sleeping for " + str(secs / n) + " seconds")
                sleep(secs / n)
            else:
                print("FARM ENDED")

user = get_user_from_json(USERNAME)

multifarm_iteration([user], [True], 1)

save_user_to_json(user)