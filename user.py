import gender
import calc_bot
import instaloader
import time
from time import sleep
import os
from threading import Thread
from datetime import datetime
import random
from config import *
import json
from datetime import date

def str_to_date(s):
    y = int(s.split('-')[0])
    m = int(s.split('-')[1])
    d = int(s.split('-')[2])
    return date(y, m, d)

def get_user_from_json(username):
    json_user_data = {}
    with open('users/{}.json'.format(username), 'r') as file:
        json_user_data = json.load(file)
    return json_user_data

def save_user_to_json(user):
    with open('users/{}.json'.format(user['username']), 'w') as file:
        json.dump(user, file)


def add_old_used(username, used_username):
    user = get_user_from_json(username)
    user['full_used'].append({'username': used_username, 'common': 4, 'followers': 300, 'following': 300,
    'date': str(date(2020, 1, 1)), 'farmed': False})
    save_user_to_json(user)
    print(len(user['full_used']))

def add_new_used(username, new_used_user, common=4, followers=300, following=300):
    user = get_user_from_json(username)
    user['full_used'].append({'username': username, 'common': common, 'followers': followers, 'following': following, 'date': str(datetime.date(datetime.now())), 'farmed': False})
    save_user_to_json(user)

def good_stats(followers, following, max_followers=2000, min_followers=150, max_following=700, min_following=100, max_ratio=5, min_ratio=0.5):
    return followers > min_followers and followers < max_followers and following > min_following and following < max_following and followers / following > min_ratio and followers / following < max_ratio

def most_common_by_files(username):
    user = get_user_from_json(username)
    dct = {}
    for filename in os.listdir('people_followers'):
        if filename[:-4] in user['followers']:
            cur = open('people_followers/' + filename, 'r')
            for i in cur:
                s = i[:-1]
                if s in dct:
                    dct[s] += 1
                else:
                    dct[s] = 1
            cur.close()
    b = []
    used = []
    for i in user['full_used']:
        used.append(i['username'])
    for i in dct:
        if gender.check(i, user['farm_gender']) and i not in used:
            b.append((dct[i], i))
    b.sort()
    b.reverse()
    user['most_common'] = []
    for i, j in b:
        user['most_common'].append([j, i, 0, 0])
    save_user_to_json(user)

def add_blacklist(username, blacklist):
    for i in blacklist:
        add_old_used(username, i)

def add_good_bad_guys(username, good):
    user = get_user_from_json(username)
    for i in good:
        user['good_bad_guys'].append(i)
    save_user_to_json(user)

def get_bad_guys(username):
    user = get_user_from_json(username)
    view_bot = calc_bot.CalculusBot(username, user['password'])
    a = view_bot.bad_guys(username)
    real_bad = []
    for i in a:
        if i not in user['good_bad_guys']:
            real_bad.append(i)
    user['temp_bad_guys'] = real_bad
    print("BAD GUYS OF " + username + " ARE:")
    print(real_bad)
    user['temp_bad_guys_ind'] = 0
    save_user_to_json(user)

def full_restart(username):
    user = get_user_from_json(username)
    user['find_people_ind'] = 0
    user['ff_ind'] = 0
    user['farm_ind'] = 0
    user['most_common'] = []
    user['followers'] = []
    user['temp_bad_guys'] = []
    user['temp_bad_guys_ind'] = 0
    view_bot = calc_bot.CalculusBot(username, user['password'])
    a = view_bot.followers_list(username)
    b = view_bot.followers(username)
    c = view_bot.followees(username)
    print('Full restart on client {}, just found his {} followers: {}'.format(username, len(a), a))
    user['info'] += " ... restart: " + str(datetime.date(datetime.now())) + ", followers: " + \
        str(b) + ", following: " + str(c)
    for i in a:
        user['followers'].append(i)
    random.shuffle(user['followers'])
    save_user_to_json(user)

def get_farm_stats(username, date_start='2000-01-01', date_end=str(datetime.date(datetime.now())), recalc=False, username_to_calc='', password_to_calc='', proxy=DEFAULT_PROXY):
    user = get_user_from_json(username)
    if username_to_calc == '':
        username_to_calc = username
        password_to_calc = user['password']
    date_start = str_to_date(date_start)
    date_end = str_to_date(date_end)
    if recalc:
        view_bot = calc_bot.CalculusBot(username_to_calc, password_to_calc, proxy)
        user['followers'] = view_bot.followers_list(username)
    for i in user['full_used']:
        if i['username'] in user['followers']:
            i['farmed'] = True
    farming = []
    for i in user['full_used']:
        date_farming = str_to_date(i['date'])
        if date_farming >= date_start and date_farming <= date_end:
            farming.append(i)
    ttl_farming = len(farming)
    ttl_farmed = 0
    boys_farming = 0
    girls_farming = 0
    boys_farmed = 0
    girls_farmed = 0
    avg_followers = 0
    avg_following = 0
    avg_common = 0
    for i in farming:
        if gender.isGirl(i['username']):
            girls_farming += 1
        elif gender.isBoy(i['username']):
            boys_farming += 1
        if i['farmed']:
            ttl_farmed += 1
            avg_followers += i['followers']
            avg_following += i['following']
            avg_common += i['common']
            if gender.isGirl(i['username']):
                girls_farmed += 1
            elif gender.isBoy(i['username']):
                boys_farmed += 1
    save_user_to_json(user)
    print('Farm stats on', username.upper(), 'in period from', date_start, 'to', date_end)
    print('Total farming:', ttl_farming, '  ', 'Total farmed:', ttl_farmed)
    if ttl_farmed == 0:
        return
    avg_followers //= ttl_farmed
    avg_following //= ttl_farmed
    avg_common //= ttl_farmed
    print('Conversion:', str(round(100 * ttl_farmed / ttl_farming)) + '%')
    print('Avg followers:', avg_followers, '  ', 'Avg following:', avg_following, '  ', 'Avg common:', avg_common)
    if boys_farming + girls_farming > 0:
        print('About genders')
        girls = round(100 * girls_farming / (girls_farming + boys_farming))
        boys = 100 - girls
        print('Farming:', 'girls part -', str(girls) + '%', '  boys part -', str(boys) + '%')
    if boys_farmed + girls_farmed > 0:
        girls = round(100 * girls_farmed / (girls_farmed + boys_farmed))
        boys = 100 - girls
        print('Farmed:', 'girls part -', str(girls) + '%', '  boys part -', str(boys) + '%')

if __name__ == '__main__':
    # pass

    # add_blacklist('bugabrows', ['danilkorolkov'])

    get_farm_stats('bugabrows', '2020-10-19', username_to_calc='boris_nikitin_johnson', password_to_calc='jfn3FF3jd', recalc=True, proxy={'host': '193.187.146.145', 'port': 8000, 'username': 'TMBmYc', 'password': 'Za5u2k'})
    # full_restart('melnikoff_oleg')
    # full_restart('nazarchansky')
