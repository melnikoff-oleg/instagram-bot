import gender
import calc_bot
import instaloader
import time
from time import sleep
import os
from threading import Thread
from datetime import datetime
import random
from constants import *
import json
from datetime import date

def str_to_date(s):
    y = int(s.split('-')[0])
    m = int(s.split('-')[1])
    d = int(s.split('-')[2])
    return date(y, m, d)

def get_user_from_json(username):
    file = open('users/' + username + '.json', 'r')
    json_user_data = json.load(file)
    user = User(**json_user_data)
    return user

def save_user_to_json(user):
    file = open('users/' + user.username + '.json', 'w')
    user_as_dict = {'username': user.username, 'password': user.password, 'workers': user.workers,
                    'farm_gender': user.farm_gender, 'max_followers': user.max_followers, 'min_followers': user.min_followers,
                    'max_following': user.max_following, 'min_following': user.min_following, 'max_ratio': user.max_ratio,
                    'min_ratio': user.min_ratio, 'find_people_ind': user.find_people_ind,
                    'ff_ind': user.ff_ind, 'farm_ind': user.farm_ind, 'full_used': user.full_used, 'followers': user.followers,
                    'good_bad_guys': user.good_bad_guys, 'temp_bad_guys': user.temp_bad_guys,
                    'temp_bad_guys_ind': user.temp_bad_guys_ind, 'info': user.info, 'most_common': user.most_common}
    json.dump(user_as_dict, file)
    file.close()


class User():

    def __init__(self, username, password, workers, farm_gender, max_followers, min_followers, max_following,
                 min_following, max_ratio, min_ratio, username_to_calc='', password_to_calc='', most_common=[],
                 full_used=[], good_bad_guys=[], ff_ind=0, find_people_ind=0, farm_ind=0, followers=[], temp_bad_guys=[],
                 temp_bad_guys_ind=0, info=''):
        self.username = username
        self.password = password
        self.find_people_ind = find_people_ind
        self.ff_ind = ff_ind
        self.farm_ind = farm_ind
        self.full_used = full_used
        self.used = []
        for i in full_used:
            self.used.append(i['username'])
        self.most_common = most_common
        self.workers = workers
        self.followers = followers
        self.max_followers = max_followers
        self.min_followers = min_followers
        self.max_following = max_following
        self.min_following = min_following
        self.max_ratio = max_ratio
        self.min_ratio = min_ratio
        self.farm_gender = farm_gender
        self.good_bad_guys = good_bad_guys
        self.temp_bad_guys = temp_bad_guys
        self.temp_bad_guys_ind = temp_bad_guys_ind
        self.info = info
        self.temp_ff_all = {}
        if len(followers) == 0:
            view_bot = calc_bot.CalculusBot(username_to_calc, password_to_calc)
            a = view_bot.followers_list(username)
            b = view_bot.followers(username)
            c = view_bot.followees(username)
            self.info = "start: " + \
                str(datetime.date(datetime.now())) + \
                ", followers: " + str(b) + ", following: " + str(c)
            for i in a:
                self.used.append(i)
                self.followers.append(i)
            random.shuffle(self.followers)

    def add_old_used(self, username):
        self.used.append(username)
        self.full_used.append({'username': username, 'common': 4, 'followers': 300, 'following': 300,
        'date': str(datetime.date(2020, 1, 1)), 'farmed': False})

    def add_new_used(self, ind):
        username, common, followers, following = self.most_common[ind]
        self.used.append(username)
        self.full_used.append({'username': username, 'common': common, 'followers': followers, 'following': following,
        'date': str(datetime.date(datetime.now())), 'farmed': False})

    def find_people_by_worker(self, start, length, username, password):
        L = instaloader.Instaloader()
        L.login(username, password)
        for i in range(start, start + length):
            cur_ind = i - start
            try:
                if not os.path.exists("people_followers/" + self.followers[i] + ".txt"):
                    profile = instaloader.Profile.from_username(
                        L.context, self.followers[i])
                    if profile.followers < 1100:
                        cur_followers = []
                        for j in profile.get_followers():
                            cur_followers.append(j.username)
                        if len(cur_followers) > 0:
                            cur_file = open(
                                'people_followers/' + self.followers[i] + '.txt', 'w')
                            for j in cur_followers:
                                cur_file.write(j + '\n')
                            cur_file.close()
                            print(self.followers[i] + " collected by " +
                                  username + " it's " + str(cur_ind) + "/" + str(length))
                        else:
                            print("private " + self.followers[i] + " was not collected by " +
                                  username + " it's " + str(cur_ind) + "/" + str(length))
                else:
                    file = open("people_followers/" +
                                self.followers[i] + ".txt", 'r')
                    x = file.readlines()
                    file.close()
                    if len(x) == 0:
                        profile = instaloader.Profile.from_username(
                            L.context, self.followers[i])
                        if profile.followers < 1000:
                            cur_followers = []
                            for j in profile.get_followers():
                                cur_followers.append(j.username)
                            if len(cur_followers) > 0:
                                cur_file = open(
                                    'people_followers/' + self.followers[i] + '.txt', 'w')
                                for j in cur_followers:
                                    cur_file.write(j + '\n')
                                cur_file.close()
                                print("private " + self.followers[i] + " collected by " + username + " it's " + str(
                                    cur_ind) + "/" + str(length))
                            else:
                                print("private " + self.followers[i] + " was not collected by " + username + " it's " + str(
                                    cur_ind) + "/" + str(length))
            except instaloader.exceptions.ProfileNotExistsException:
                print("Oops!  " + str(i) + " Not founded")
            except Exception as e:
                print(e)
                print("worker " + username + " sleeping for 10 sec")
                time.sleep(10)

    def find_people(self, n):
        n = min(n, len(self.followers) - self.find_people_ind)
        threads = []
        add = n % len(self.workers)
        for i in range(len(self.workers)):
            d = int(n / len(self.workers))
            if i < add:
                d += 1
            thread = Thread(target=self.find_people_by_worker, args=(
                self.find_people_ind, d, self.workers[i][0], self.workers[i][1]))
            print("IN THIS THREAD WE WILL CALL FLWS OF")
            print(d)
            threads.append(thread)
            self.find_people_ind += d
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        if(self.workers[0][0] == self.username):
            print("finding of " + str(n) +
                  " privates on the " + self.username + " done")
        else:
            print("finding of " + str(n) +
                  " people on the " + self.username + " done")

    def calc_ff_by_worker(self, start, length, username, password):
        L = instaloader.Instaloader()
        L.login(username, password)
        for i in range(start, start + length):
            z = self.most_common[i][2]
            cur = self.most_common[i][0]
            if z > 0:
                continue
            if cur in self.temp_ff_all:
                x = self.temp_ff_all[cur][0]
                y = self.temp_ff_all[cur][1]
                self.most_common[i][2] = x
                self.most_common[i][3] = y
                continue
            try:
                profile = instaloader.Profile.from_username(L.context, cur)
                x = profile.followers
                y = profile.followees
                self.most_common[i][2] = x
                self.most_common[i][3] = y
                self.temp_ff_all[cur] = [x, y]
                cur_ind = i - start
                print("ff of " + cur + " calced by " + username +
                      " it's " + str(cur_ind) + "/" + str(length))
            except Exception as e:
                print(e)

    def calc_ff(self, n):
        file = open('ff_all.txt', 'r')
        for line in file:
            try:
                x = int(line.split(' ')[1])
                y = int(line.split(' ')[2])
                cur = line.split(' ')[0]
                self.temp_ff_all[cur] = [x, y]
            except Exception as e:
                print(e)
        file.close()
        n = min(n, len(self.most_common) - self.ff_ind)
        threads = []
        add = n % len(self.workers)
        for i in range(len(self.workers)):
            d = int(n / len(self.workers))
            if i < add:
                d += 1
            thread = Thread(target=self.calc_ff_by_worker, args=(
                self.ff_ind, d, self.workers[i][0], self.workers[i][1]))
            threads.append(thread)
            self.ff_ind += d
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        file = open('ff_all.txt', 'w')
        for i in self.temp_ff_all:
            file.write(
                i + ' ' + str(self.temp_ff_all[i][0]) + ' ' + str(self.temp_ff_all[i][1]) + '\n')
        file.close()
        self.temp_ff_all = {}
        print("calcing ff of " + str(n) +
              " people on the " + self.username + " done")

    def good_stats(self, i):
        followers = self.most_common[i][2]
        following = self.most_common[i][3]
        return followers > self.min_followers and followers < self.max_followers and following > self.min_following and following < self.max_following and followers / following > self.min_ratio and followers / following < self.max_ratio

    def most_common_by_files(self):
        dct = {}
        for filename in os.listdir('people_followers'):
            if filename[:-4] in self.followers:
                cur = open('people_followers/' + filename, 'r')
                for i in cur:
                    s = i[:-1]
                    if s in dct:
                        dct[s] += 1
                    else:
                        dct[s] = 1
                cur.close()
        b = []
        for i in dct:
            if gender.check(i, self.farm_gender) and i not in self.used:
                b.append((dct[i], i))
        b.sort()
        b.reverse()
        self.most_common = []
        for i, j in b:
            self.most_common.append([j, i, 0, 0])

    def add_blacklist(self, blacklist):
        for i in blacklist:
            self.used.append(i)

    def add_good_bad_guys(self, good):
        for i in good:
            self.good_bad_guys.append(i)

    def get_bad_guys(self):
        view_bot = calc_bot.CalculusBot(self.username, self.password)
        a = view_bot.bad_guys(self.username)
        real_bad = []
        for i in a:
            if i not in self.good_bad_guys:
                real_bad.append(i)
        self.temp_bad_guys = real_bad
        print("BAD GUYS OF " + self.username + " ARE:")
        print(real_bad)
        self.temp_bad_guys_ind = 0

    def full_restart(self, username_to_calc='', password_to_calc=''):
        if username_to_calc == '':
            username_to_calc = self.username
            password_to_calc = self.password
        self.find_people_ind = 0
        self.ff_ind = 0
        self.farm_ind = 0
        self.most_common = []
        self.followers = []
        self.temp_ff_all = {}
        view_bot = calc_bot.CalculusBot(username_to_calc, password_to_calc)
        a = view_bot.followers_list(self.username)
        b = view_bot.followers(self.username)
        c = view_bot.followees(self.username)
        self.info += "...restart: " + str(datetime.date(datetime.now())) + ", followers: " + \
            str(b) + ", following: " + str(c)
        for i in a:
            self.followers.append(i)
        random.shuffle(self.followers)

    def find_people_privates(self, n):
        if self.find_people_ind == len(self.followers):
            self.find_people_ind = 0
        temp_workers = self.workers
        self.workers = [[self.username, self.password]]
        self.find_people(n)
        self.workers = temp_workers

    def collect_old_used(self):
        file = open(self.username + '/used.txt', 'r')
        a = file.readlines()
        file.close()
        for i in a:
            username = i.split(' ')[0]
            if username not in self.used:
                self.add_old_used(username)

    def get_farm_stats(self, date_start='2000-01-01', date_end=str(datetime.date(datetime.now()))):
        date_start = str_to_date(date_start)
        date_end = str_to_date(date_end)
        view_bot = calc_bot.CalculusBot(self.username, self.password)
        self.followers = view_bot.followers_list(self.username)
        for i in self.full_used:
            if i['username'] in self.followers:
                i['farmed'] = True
        farming = []
        for i in self.full_used:
            date_farming = str_to_date(i['date'])
            if date_farming >= date_start and date_farming <= date_end:
                farming.append(i)
        ttl_farming = len(farming)
        ttl_farmed = 0
        boys = 0
        girls = 0
        avg_followers = 0
        avg_following = 0
        for i in farming:
            if i['farmed']:
                ttl_farmed += 1
                avg_followers += i['followers']
                avg_following += i['following']
                if gender.isGirl(i['username']):
                    girls += 1
                elif gender.isBoy(i['username']):
                    boys += 1
        print('Farm stats on', self.username.capitalize(), 'in period from', date_start, 'to', date_end)
        print('Total farming', ttl_farming)
        print('Total farmed', ttl_farmed)
        if ttl_farmed == 0:
            return
        avg_followers //= ttl_farmed
        avg_following //= ttl_farmed
        print('Conversion:', ttl_farmed / ttl_farming)
        print('Avg followers:', avg_followers)
        print('Avg following:', avg_following)
        if boys + girls > 0:
            print('Boys:', boys, 'Girls: ', girls)
            print('Girls percente:', str(100 * girls / (girls + boys)) + '%', 'Boys percente:', str(100 * boys / (girls + boys)) + '%')


if __name__ == '__main__':


    users_arr = []
    for i in USERS:
        users_arr.append(get_user_from_json(i['username']))

    # for k in range(2):
    #     for i in users_arr:
    #         i.find_people(50)

    for i in users_arr:
        if i.username == 'nazarchansky':
            continue
        # i.collect_old_used()
        # i.most_common_by_files()
        # print(i.username, i.farm_ind)
        print(i.username)
        i.get_farm_stats('2020-09-24')
        print()
        print()
        print()

    for i in users_arr:
        save_user_to_json(i)



    # user_id = 1
    # username = USERS[user_id]['username']
    # password = USERS[user_id]['password']
    # print(username, password)
    # print("LOL")
    """user = User(username, password, [['kamshot3', 'pizdets6989']], 
    2, 2100, 150, 700, 120, 5, 0.5, username, password)
    save_pickle(user)"""

    #user = get_pickle(username)
    #print("KEK")
    #user.find_people_ind = 0
    #user.workers = [['shkur_dolbil', 'Pidor239']]
    #user.find_people_ind = 0
    #user.find_people(100)
    #user.find_people_privates(700)
    #user.most_common_by_files()
    #user.ff_ind = 0
    #user.calc_ff(10)

    # print(user.most_common[:40])
    # print(user.find_people_ind)
    # print(user.ff_ind)
    #print(user.followers)
    # print(len(user.followers))

    #save_pickle(user)
    # сделал по 300 на двух
