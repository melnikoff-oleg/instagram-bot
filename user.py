import gender
import calc_bot
import instaloader
import time
from time import sleep
import os 
from threading import Thread
from datetime import datetime
import random
from pickle_handle import *
from constants import *

#с pickle есть некоторые проблемы, проще хранить все в JSON дампах, там хотя бы все видно

class User():

    def __init__(self, username, password, workers, farm_gender, max_followers, min_followers, max_following, 
    min_following, max_ratio, min_ratio, username_to_calc, password_to_calc):
        self.username = username
        self.password = password
        self.find_people_ind = 0
        self.ff_ind = 0
        self.farm_ind = 0
        self.used = [username]
        self.most_common = []
        self.workers = workers
        self.followers = []
        self.temp_ff_all = {}
        self.max_followers = max_followers
        self.min_followers = min_followers
        self.max_following = max_following
        self.min_following = min_following
        self.max_ratio = max_ratio
        self.min_ratio = min_ratio
        self.farm_gender = farm_gender
        self.good_bad_guys = []
        self.temp_bad_guys = []
        self.temp_bad_guys_ind = 0
        view_bot = calc_bot.CalculusBot(username_to_calc, password_to_calc)
        a = view_bot.followers_list(username)
        b = view_bot.followers(username)
        c = view_bot.followees(username)
        self.info = "start " +  str(datetime.date(datetime.now())) + " " + str(b) + " followers " + str(c) + " following"
        for i in a:
            self.used.append(i)
            self.followers.append(i)
        random.shuffle(self.followers)

        
        

    def find_people_by_worker(self, start, length, username, password):
        L = instaloader.Instaloader()
        L.login(username, password)
        for i in range(start, start + length):
            cur_ind = i - start
            try:
                if not os.path.exists("people_followers/" + self.followers[i] + ".txt"):
                    profile = instaloader.Profile.from_username(L.context, self.followers[i])
                    if profile.followers < 1100:
                        cur_followers = []
                        for j in profile.get_followers():
                            cur_followers.append(j.username)
                        if len(cur_followers) > 0:
                            cur_file = open('people_followers/' + self.followers[i] + '.txt', 'w')
                            for j in cur_followers:
                                cur_file.write(j + '\n')
                            cur_file.close()
                            print(self.followers[i] + " collected by " + username + " it's " + str(cur_ind) + "/" + str(length))
                        else:
                            print("private " + self.followers[i] + " was not collected by " + username + " it's " + str(cur_ind) + "/" + str(length))
                else:
                    file = open("people_followers/" + self.followers[i] + ".txt", 'r')
                    x = file.readlines()
                    file.close()
                    if len(x) == 0:
                        profile = instaloader.Profile.from_username(L.context, self.followers[i])
                        if profile.followers < 1000:
                            cur_followers = []
                            for j in profile.get_followers():
                                cur_followers.append(j.username)
                            if len(cur_followers) > 0:
                                cur_file = open('people_followers/' + self.followers[i] + '.txt', 'w')
                                for j in cur_followers:
                                    cur_file.write(j + '\n')
                                cur_file.close()
                                print("private " + self.followers[i] + " collected by " + username + " it's " + str(cur_ind) + "/" + str(length))
                            else:
                                print("private " + self.followers[i] + " was not collected by " + username + " it's " + str(cur_ind) + "/" + str(length))
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
            thread = Thread(target=self.find_people_by_worker, args=(self.find_people_ind, d, self.workers[i][0], self.workers[i][1]))
            print("IN THIS THREAD WE WILL CALL FLWS OF")
            print(d)
            threads.append(thread)
            self.find_people_ind += d
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        if(self.workers[0][0] == self.username):
            print("finding of " + str(n) + " privates on the " + self.username + " done")
        else:
            print("finding of " + str(n) + " people on the " + self.username + " done")

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
                print("ff of " + cur + " calced by " + username + " it's " + str(cur_ind) + "/" + str(length))
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
            thread = Thread(target=self.calc_ff_by_worker, args=(self.ff_ind, d, self.workers[i][0], self.workers[i][1]))
            threads.append(thread)
            self.ff_ind += d
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        file = open('ff_all.txt', 'w')
        for i in self.temp_ff_all:
            file.write(i + ' ' + str(self.temp_ff_all[i][0]) + ' ' + str(self.temp_ff_all[i][1]) + '\n')
        file.close()
        self.temp_ff_all = {} 
        print("calcing ff of " + str(n) + " people on the " + self.username + " done")

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
        self.info += "\nrestart " +  str(datetime.date(datetime.now())) + " " + str(b) + " followers " + str(c) + " following"
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
        file = open(username + '/used.txt', 'r')
        a = file.readlines()
        file.close()
        for i in a:
            cur = i.split(' ')[0]
            if cur not in self.used:
                self.used.append(cur)


# def __init__(self, username, password, workers, farm_gender, max_followers, min_followers, max_following, 
# min_following, max_ratio, min_ratio, username_to_calc, password_to_calc):

if __name__ == '__main__':
    username = USERNAME
    password = PASSWORD
    print("LOL")
    """user = User(username, password, [['jerry_piskoff', 'Pidor239']], 
    2, 2000, 150, 700, 100, 10, 0.4, username, password)
    save_pickle(user)"""

    """user = get_pickle(username)
    print("KEK")
    user.find_people_ind = 0
    user.find_people(2)
    # user.find_people_privates(700)
    user.most_common_by_files()
    user.ff_ind = 0
    user.calc_ff(10)

    print(user.most_common[:40])
    print(user.ff_ind)
    print(user.followers)
    print(len(user.followers))

    save_pickle(user)"""