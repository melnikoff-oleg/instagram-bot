from threading import Thread
import json
import instaloader
from full_pipeline import *
from random import randint

def get_exit_flag():
    exit = True
    with open('exit_flag.json', 'r') as file:
        json_data = json.load(file)
        exit = json_data['exit']
    return exit


threads = []

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

for nomad in NOMADS:
    thread = Thread(target=nomads_work, args=(nomad['username'], nomad['password'], nomad['proxy']))
    threads.append(thread)
for i in range(len(threads)):
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()
    