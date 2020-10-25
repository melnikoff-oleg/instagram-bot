import json
from datetime import datetime
from datetime import date
import calc_bot
import random
from time import sleep
import instaloader
import os
import gender
import time
from config import *

def get_best_paladin():
    filenamemin = -1
    min_len = 1000

    for filename in os.listdir('paladins/'):
        with open('paladins/{}'.format(filename), 'r') as file:
            json_farm_data = json.load(file)
            if len(json_farm_data) < min_len:
                min_len = len(json_farm_data)
                filenamemin = filename


    if filenamemin == -1:
        print('There is no farm chrome instances, so current client gets nothing')
        return -1
    else:
        number = filenamemin.split('_')[-1]
        number = int(number.split('.')[0])
        return number

def create_user_json(username, password, farm_gender=2, max_followers=2000, min_followers=150, max_following=700, min_following=100, max_ratio=5, min_ratio=0.5, good_bad_guys=[]):
    most_common = []
    full_used = []
    ff_ind = 0
    find_people_ind = 0
    farm_ind = 0
    followers = []
    temp_bad_guys = []
    temp_bad_guys_ind = 0
    info = ''
    paladin_id = get_best_paladin()
    proxy = PALADINS[paladin_id]['proxy']

    view_bot = calc_bot.CalculusBot(username, password, proxy)
    followers = view_bot.followers_list(username)
    followers_amount = view_bot.followers(username)
    followees_amount = view_bot.followees(username)
    print('Followers list, followers and following of {} calculated'.format(username))
    info = 'start: {}, followers: {}, following: {}'.format(datetime.date(datetime.now()), followers_amount, followees_amount)
    for i in followers:
        full_used.append({'username': i, 'common': 4, 'followers': 300, 'following': 300, 'date': str(date(2020, 1, 1)), 'farmed': True})
    random.shuffle(followers)
    with open('users/{}.json'.format(username), 'w') as file:
        user_as_dict = {'username': username, 'password': password, 'farm_gender': farm_gender, 'max_followers':    max_followers, 'min_followers': min_followers,
                        'max_following': max_following, 'min_following': min_following, 'max_ratio': max_ratio,
                        'min_ratio': min_ratio, 'find_people_ind': find_people_ind,
                        'ff_ind': ff_ind, 'farm_ind': farm_ind, 'paladin_id': paladin_id, 'full_used': full_used, 'followers': followers,
                        'good_bad_guys': good_bad_guys, 'temp_bad_guys': temp_bad_guys,
                        'temp_bad_guys_ind': temp_bad_guys_ind, 'info': info, 'most_common': most_common}
        json.dump(user_as_dict, file)
        print('New client {} has been created!!!'.format(username))
    find_people(username)


def get_user_from_json(username):
    json_user_data = {}
    with open('users/{}.json'.format(username), 'r') as file:
        json_user_data = json.load(file)
    return json_user_data

def save_user_to_json(user):
    with open('users/{}.json'.format(user['username']), 'w') as file:
        json.dump(user, file)

def add_find_people_blocks(followers_blocks):
    with open('ruins/find_people_blocks.json', 'r') as file:
        json_blocks_data = json.load(file)

    json_blocks_data['find_people_blocks'] = json_blocks_data['find_people_blocks'] + followers_blocks
    with open('ruins/find_people_blocks.json', 'w') as file:
        json.dump(json_blocks_data, file)

def find_people(username):
    print('Started finding people on client {}'.format(username))
    user = get_user_from_json(username)
    followers_block_size = RUIN_BLOCK_SIZE[DEBUG]
    followers_blocks = []
    cur_block = {'followers': [], 'username': username, 'last_block': False}
    people_amount = len(user['followers'])
    if DEBUG:
        people_amount = min(people_amount, FIND_PEOPLE_DEBUG)
    for i, follower in enumerate(user['followers']):
        cur_block['followers'].append(follower)
        if people_amount == i + 1:
            cur_block['last_block'] = True
        if len(cur_block['followers']) == followers_block_size or people_amount == i + 1:
            followers_blocks.append(cur_block.copy())
            cur_block['followers'] = []
        if people_amount == i + 1:
            break
    add_find_people_blocks(followers_blocks)
    print('Find people blocks of client {} were successfully added to Ruins JSON'.format(username))

def get_find_people_block(ruin_name):
    with open('ruins/find_people_blocks.json', 'r') as file:
        json_blocks_data = json.load(file)

    while len(json_blocks_data['find_people_blocks']) == 0:
        print('No available find people blocks in here')
        sleep_time = 600
        if DEBUG:
            sleep_time = 30
        print('Ruin {} sleeping for {} secs'.format(ruin_name, sleep_time))
        sleep(sleep_time)
        with open('ruins/find_people_blocks.json', 'r') as file:
            json_blocks_data = json.load(file)
    block = json_blocks_data['find_people_blocks'].pop(0)
    with open('ruins/find_people_blocks.json', 'w') as file:
        json.dump(json_blocks_data, file)
    print('Just get 1 find people block for client {}, processing by ruin {}'.format(block['username'], ruin_name))
    return block


def process_find_people_block(instaloader_session, block, ruin_name):
    for cur_ind, follower in enumerate(block['followers']):
        try:
            with open("people_followers/" + follower + ".txt", 'r') as file:
                x = file.readlines()
            if len(x) > 0:
                continue
        except Exception as e:
            print(e)

        try:
            profile = instaloader.Profile.from_username(instaloader_session.context, follower)
            if profile.followers < 1100:
                cur_followers = []
                for j in profile.get_followers():
                    cur_followers.append(j.username)
                if len(cur_followers) > 0:
                    cur_file = open(
                        'people_followers/' + follower + '.txt', 'w')
                    for j in cur_followers:
                        cur_file.write(j + '\n')
                    cur_file.close()
                    print(follower + " collected by " +
                            ruin_name + " it's " + str(cur_ind) + "/" + str(len(block['followers'])) + ' in current block for ' + block['username'] + 'user')
                else:
                    print("private " + follower + " was not collected by " +
                            ruin_name + " it's " + str(cur_ind) + "/" + str(len(block['followers'])) + ' in current block for ' + block['username'] + 'user')
        except instaloader.exceptions.ProfileNotExistsException:
            print("Oops!  " + str(follower) + " Not founded")
        except Exception as e:
            print(e)
            print("Ruin " + ruin_name + " sleeping for 1 min")
            sleep(60)
    print('Ruin {} finished current block for {} user'.format(ruin_name, block['username']))
    if block['last_block']:
        finish_find_people(block['username'])
    sleep_time = RUIN_SLEEP_TIME[DEBUG]
    print('Ruin {} sleeping for {} secs after block calculation'.format(ruin_name, sleep_time))
    sleep(sleep_time)

def finish_find_people(username):
    user = get_user_from_json(username)
    used = []
    for i in user['full_used']:
        used.append(i['username'])
    dct = {}
    for filename in os.listdir('people_followers'):
        if filename[:-4] in user['followers']:
            with open('people_followers/' + filename, 'r') as cur:
                for i in cur:
                    s = i[:-1]
                    if s in dct:
                        dct[s] += 1
                    else:
                        dct[s] = 1
    b = []
    for i in dct:
        if gender.check(i, user['farm_gender']) and i not in used:
            b.append((dct[i], i))
    b.sort()
    b.reverse()
    most_common = []
    for i, j in b:
        most_common.append([j, i, 0, 0])
    
    upper_bound = min(len(most_common), 1000)
    if DEBUG:
        upper_bound = min(upper_bound, CALC_PEOPLE_DEBUG)
    user['most_common'] = most_common[:upper_bound]
    save_user_to_json(user)
    print('Finding people and creating most_common on {0} finished!!!'.format(username))
    calc_people(user['username'])





def add_calc_people_blocks(followers_blocks):
    with open('nomads/calc_people_blocks.json', 'r') as file:
        json_blocks_data = json.load(file)
    json_blocks_data['calc_people_blocks'] = json_blocks_data['calc_people_blocks'] + followers_blocks
    with open('nomads/calc_people_blocks.json', 'w') as file:
        json.dump(json_blocks_data, file)

def calc_people(username):
    user = get_user_from_json(username)
    followers_block_size = NOMAD_BLOCK_SIZE[DEBUG]
    followers_blocks = []
    cur_block = {'followers': [], 'username': username, 'last_block': False}
    people_amount = len(user['most_common'])
    if DEBUG:
        people_amount = min(people_amount, CALC_PEOPLE_DEBUG)

    for ind, follower in enumerate(user['most_common']):
        cur_block['followers'].append(follower)
        if ind + 1 == people_amount:
            cur_block['last_block'] = True
        if len(cur_block['followers']) == followers_block_size or ind + 1 == people_amount:
            followers_blocks.append(cur_block.copy())
            cur_block['followers'] = []
        if ind + 1 == people_amount:
            break
    add_calc_people_blocks(followers_blocks)
    print('Calc people blocks of client {} successfully added to nomads pool'.format(username))

def get_ff_all():
    with open('ff_calc/ff_all.txt', 'r') as file:
        ff_all = {}
        for line in file:
            try:
                x = int(line.split(' ')[1])
                y = int(line.split(' ')[2])
                cur = line.split(' ')[0]
                ff_all[cur] = [x, y]
            except Exception as e:
                print(e)
    return ff_all

def save_ff_all(ff_all):
    with open('ff_calc/ff_all.txt', 'w') as file:
        for i in ff_all:
            file.write(i + ' ' + str(ff_all[i][0]) + ' ' + str(ff_all[i][1]) + '\n')


def get_calc_people_block(nomad_name):
    with open('nomads/calc_people_blocks.json', 'r') as file:
        json_blocks_data = json.load(file)
    while len(json_blocks_data['calc_people_blocks']) == 0:
        print('No available calc people blocks in here')
        sleep_time = 600
        if DEBUG:
            sleep_time = 30
        print('Nomad {} sleeping for {} secs, waiting for new calc people blocks'.format(nomad_name, sleep_time))
        sleep(sleep_time)
        with open('nomads/calc_people_blocks.json', 'r') as file:
            json_blocks_data = json.load(file)
    block = json_blocks_data['calc_people_blocks'].pop(0)
    with open('nomads/calc_people_blocks.json', 'w') as file:
        json.dump(json_blocks_data, file)
    return block

def process_calc_people_block(instaloader_session, block, nomad_name):

    print('Nomad {} started processing new block for {} client'.format(nomad_name, block['username']))
    length = min(len(block['followers']), 2)
    print('Here you can check beginning of this block {}'.format(block['followers'][:length]))
    temp_ff_all = get_ff_all()
    ttl_new = 0
    for cur_ind, cur in enumerate(block['followers']):
        if not cur[0] in temp_ff_all:
            ttl_new += 1
            try:
                follower = cur[0]
                profile = instaloader.Profile.from_username(instaloader_session.context, follower)
                x = profile.followers
                y = profile.followees
                temp_ff_all[follower] = [x, y]
                print("ff of " + follower + " calced by Nomad " + nomad_name + " it's " + str(cur_ind) + "/" + str(len(block['followers'])) + ' in current block for ' + block['username'] + ' user')
            except Exception as e:
                print('Following error occured in the Nomad ' + nomad_name + ' work, while calcing ff of {}'.format(cur[0]))
                print(e)
    save_ff_all(temp_ff_all)
    print('Nomad ' + nomad_name + ' finished current block for ' + block['username'] + ' user')
    if block['last_block']:
        finish_calc_people(block['username'], nomad_name)
    sleep_time = round(NOMAD_SLEEP_TIME[DEBUG] * (ttl_new / len(block['followers'])))
    print("Nomad {} sleeping for {} secs after block calculation".format(nomad_name, sleep_time))
    #sleep(600)
    sleep(sleep_time)

def good_stats(followers, following, max_followers=2000, min_followers=150, max_following=700, min_following=100, max_ratio=5, min_ratio=0.5):
    return followers > min_followers and followers < max_followers and following > min_following and following < max_following and followers / following > min_ratio and followers / following < max_ratio

def finish_calc_people(username, nomad_name):
    print('Now ruin {} is finishing calc people on client {}'.format(nomad_name, username))
    user = get_user_from_json(username)
    old_most_common = user['most_common']
    new_most_common = []
    ff_all = get_ff_all()
    for follower in old_most_common:
        try:
            if good_stats(ff_all[follower[0]][0], ff_all[follower[0]][1], user['max_followers'], user['min_followers'], user['max_following'], user['min_following'], user['max_ratio'], user['min_ratio']):
                new_most_common.append([follower[0], follower[1], ff_all[follower[0]][0], ff_all[follower[0]][1]])
            else:
                user['full_used'].append({'username': follower[0], 'common': follower[1], 'followers': ff_all[follower[0]][0], 'following': ff_all[follower[0]][1], 'date': str(date(2020, 1, 1)), 'farmed': False})
        except Exception as e:
            print('Error occured while finishing peop calc on client {}'.format(username))
            print(e)
    user['most_common'] = new_most_common
    save_user_to_json(user)
    print('Finishing ff calculation on ' + username)
    print('There were ' + str(len(old_most_common)) + ' persons in most_common before')
    print('Now most_common contains only ' + str(len(new_most_common)) + ' persons with good stats')
    push_client_in_farm(username)




def push_client_in_farm(username):
    start = [[2, 0], [3, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0]]
    mid_block = [[-1, -1], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4]]
    mid = []
    for i in range(14):
        mid = mid + mid_block
    mid = mid + [-1, -1]
    end = [[0, 10] for i in range(10)]
    operations = start + mid + end
    if DEBUG:
        operations = [[1, 0], [1, 1], [0, 1]]
    client_pack = {'username': username, 'operations': operations, 'last_operation': int(time.time())}
    push_json_client_in_farm(client_pack)

def push_json_client_in_farm(client_pack):
    username = client_pack['username']
    user = get_user_from_json(username)
    paladin_id = user['paladin_id']
    if paladin_id == -1:
        print('There is no farm chrome instances, so client {} gets nothing'.format(username))
        return
    filenamemin = 'farm_instance_{}.json'.format(paladin_id)
    with open('paladins/{}'.format(filenamemin), 'r') as file:
        json_farm_data = json.load(file)
    json_farm_data.append(client_pack)
    with open('paladins/{}'.format(filenamemin), 'w') as file:
        json.dump(json_farm_data, file)
    print('Client ' + client_pack['username'] + ' succesfully gets into farm!')


def one_loop_paladin_process(paladin_id, ig_bot):
    with open('paladins/farm_instance_{}.json'.format(paladin_id), 'r') as file:
        json_farm_data = json.load(file)
    argmin = -1
    min_time_last_operation = 1000000000000000
    for ind, client in enumerate(json_farm_data):
        if client['last_operation'] < min_time_last_operation:
            argmin = ind
            min_time_last_operation = client['last_operation']

    if argmin == -1:
        sleep_time = 600
        if DEBUG:
            sleep_time = 30
        print('Paladin {} have NO ready clients, so he will sleep for {} secs'.format(paladin_id, sleep_time))
        sleep(sleep_time)
        return
    client = json_farm_data[argmin]
    operations = client['operations']
    username = client['username']
    cur_operation = operations.pop(0)
    if cur_operation == [-1, -1]:
        find_bad(username)
        cur_operation = operations.pop(0)

    

    process_one_farm_operation(ig_bot, username, cur_operation)
    client['last_operation'] = int(time.time())
    operations_len = len(operations)
    if operations_len == 0:
        print('YEEEEEEEZZZZZZZZZZ')
        print('YEEEEEEEZZZZZZZZZZ')
        print('YEEEEEEEZZZZZZZZZZ')
        print('Finally finished farm on {client_name} !!!'.format(client_name=username))
        json_farm_data.pop(argmin)
        

    
    with open('paladins/farm_instance_{}.json'.format(paladin_id), 'w') as file:
        json.dump(json_farm_data, file)
    

    sleep_secs = PALADIN_SLEEP_TIME[DEBUG]
    if len(json_farm_data) > 0:
        sleep_secs /= len(json_farm_data)
    print('Paladin {paladin_id} finished 1 farm iteration on client {username} and now will sleep for {secs} secs'.format(username=username, paladin_id=paladin_id, secs=sleep_secs))
    sleep(sleep_secs)
    
    
def process_one_farm_operation(ig_bot, username, operation):
    user = get_user_from_json(username)
    ig_bot.username = user['username']
    ig_bot.password = user['password']
    ig_bot.login()
    sleep(2)
    print('Now this paladin will farm {} users on client {}, and antifarm {} users'.format(operation[0], username, operation[1]))
    while operation[0] > 0:
        operation[0] -= 1
        if user['farm_ind'] == len(user['most_common']):
            print('FARM STOPPED ON {}, most_common finished'.format({username}))
            break
        else:
            cur_farming = user['most_common'][user['farm_ind']]
            ig_bot.natural_subscribe(cur_farming[0])
            user['full_used'].append({'username':cur_farming[0], 'common': cur_farming[1], 'followers': cur_farming[2], 'following': cur_farming[3], 'date': str(datetime.date(datetime.now())), 'farmed': False})
            user['farm_ind'] += 1

    while operation[1] > 0:
        operation[1] -= 1
        if user['temp_bad_guys_ind'] == len(user['temp_bad_guys']):
            print("CUR BAD GUYS ENDED, ANTIFARM STOPPED ON {}".format(username))
        else:
            ig_bot.natural_unsubscribe(user['temp_bad_guys'][user['temp_bad_guys_ind']])
            user['temp_bad_guys_ind'] += 1
    save_user_to_json(user)
    if not ONE_USER:
        ig_bot.exit()


def find_bad(username):
    print('Now this paladin will calc bad guys of client {}'.format(username))
    user = get_user_from_json(username)
    view_bot = calc_bot.CalculusBot(user['username'], user['password'])
    a = view_bot.bad_guys(user['username'])
    real_bad = []
    for i in a:
        if i not in user['good_bad_guys']:
            real_bad.append(i)
    real_bad.reverse()
    user['temp_bad_guys'] = real_bad
    print('{} has {} bad guys:'.format(username, len(real_bad)))
    print(real_bad)
    user['temp_bad_guys_ind'] = 0
    save_user_to_json(user)


if __name__ == '__main__':
    pass
    # username = TEST_USERNAME
    # password = TEST_PASSWORD

    # create_user_json(username, password)

    # find_people(username)
    # finish_find_people(username)
    # finish_calc_people(username, password)

    # user = get_user_from_json(username)
    # ans = []
    # for i in range(200):
    #     print(user['most_common'][i][0])

    # find_people('melnikoff_oleg')
    # find_people('nazarchansky')
