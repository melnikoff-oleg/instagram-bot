from threading import Thread
import json
import instaloader
from full_pipeline import *
from random import randint
from bot import *

def get_exit_flag():
    exit = True
    with open('exit_flag.json', 'r') as file:
        json_data = json.load(file)
        exit = json_data['exit']
    return exit

def ruins_work(username, password, proxy):
    print('Ruin {} with password {} started his work'.format(username.upper(), password))
    instaloader_session = instaloader.Instaloader()
    instaloader_session.login(username, password, proxy)
    while True:
        exit = get_exit_flag()
        if exit:
            print('Ruin {} detected EXIT FLAG activated, so he breaks the loop'.format(username))
            break
        block = get_find_people_block(username)
        process_find_people_block(instaloader_session, block, username)


def nomads_work(username, password, proxy):
    print('Nomad {} started his work'.format(username.upper()))
    try:
        instaloader_session = instaloader.Instaloader()
        instaloader_session.login(username, password, proxy)
    except Exception as e:
        print('Error while logging in as nomad {}'.format(username))
        print(e)
        instaloader_session = None
    while True:
        exit = get_exit_flag()
        if exit:
            print('Nomad {} detected EXIT FLAG activated, so he breaks the loop'.format(username))
            break
        sleep(randint(0, 10))
        block = get_calc_people_block(username)
        process_calc_people_block(instaloader_session, block, username)


def paladins_work(paladin_id, proxy):
    print('Paladin {} started his work'.format(paladin_id))
    if VPS:
        from xvfbwrapper import Xvfb
        vdisplay = Xvfb()
        vdisplay.start()
    ig_bot = InstagramBot('fict', 'fict', proxy)
    while True:
        exit = get_exit_flag()
        if exit:
            print('Paladin {} detected EXIT FLAG activated, so he breaks the loop'.format(paladin_id))
            ig_bot.exit()
            break
        one_loop_paladin_process(paladin_id, ig_bot)
    if VPS:
        vdisplay.stop()



if __name__ == '__main__':
    threads = []

    for ruin in RUINS:
        thread = Thread(target=ruins_work, args=(ruin['username'], ruin['password'], ruin['proxy']))
        threads.append(thread)

    for nomad in NOMADS:
        thread = Thread(target=nomads_work, args=(nomad['username'], nomad['password'], nomad['proxy']))
        threads.append(thread)

    # for paladin_id, paladin in enumerate(PALADINS):
    #     thread = Thread(target=paladins_work, args=(paladin_id, paladin['proxy']))
    #     threads.append(thread)

    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
