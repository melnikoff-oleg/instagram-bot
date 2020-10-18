import instaloader
from config import *

class CalculusBot:
    def __init__(self, username = 'rick_dildelio', password = 'Pidor239', proxy=''):
        self.L = instaloader.Instaloader()
        self.L.login(username, password, proxy)
    
    def followers(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        return profile.followers
    
    def followees(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        return profile.followees

    def followers_list(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        a = []
        for i in profile.get_followers():
            a.append(i.username)
        return a

    def followees_list(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        a = []
        for i in profile.get_followees():
            a.append(i.username)
        return a

    def bad_guys(self, username):
        my = {'v.kaspiyskayya_11', 'fatboys.spb', 'pposya_', 'snova_teplo', 
        'sfr.spb', 'nu_sovsem_uzhe', 'paaaulzar', 'ningehot', 'tamisimonicsova', 'ilevyant', 'sir_tersy', 
        'pronishink', 'gromtrip', 'p_____gol', 'kristina_pchela', 'stasya_konstantinovaa', 'hardy.view', 
        'annyshka_17', 'kooqa', 'mareamaru', 'andrei_ganai', 'korzov', 'continental_lounge.bar', 
        'danilmatukhno', 'vikaaasok', 'frozenbite', 'markcardician', 'sanchousprivat', 'the_kyza', 
        'nastyatropi', '____dygova____', 'upsonya', 'kokorin9', '3pso.store', 
        'joli_solo', 'seme1ka', '00000000000001k', 'g.r.u.p.p.i.r.o.v.k.a', 'v_8000_', 'maximuscoach', 
        'magu.1', 'vadim_do4a_ivanov', 'gervashsergey', 'academeg', 'thenotoriousmma',
        'morgen_shtern'}
        bad = []
        for i in self.followers_list(username):
            my.add(i)
        for i in self.followees_list(username):
            if i not in my:
                x = self.followers(i)
                if x > 10000:
                    print(i + " IT'S A FAME " + str(x) + " FOLLOWERS")
                else:
                    bad.append(i)
        return bad

    def is_private(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)
        return profile.is_private()
    
    def max_intersection(self, arr):
        kek = {'kek': 0}
        cnt = 0
        for i in arr:
            for j in self.followees_list(i):
                if j not in kek:
                    kek[j] = 1
                else:
                    kek[j] += 1
            cnt += 1
            print(str(cnt) + " DONE")
        a = []
        for i in kek:
            a.append((kek[i], i))
        a.sort()
        a.reverse()
        for i, j in a:
            print(j + ' ' + str(i))
    
    def private(self, arr):
        lol = []
        for i in arr:
            if self.is_private(i):
                lol.append(i)
        return lol


if __name__ == '__main__':
    pass
    # view_bot = CalculusBot(TEST_USERNAME, TEST_PASSWORD)
    # print(view_bot.followers_list('chlenix_bulbetto'))
    # print(view_bot.followers('melnikoff_oleg'))