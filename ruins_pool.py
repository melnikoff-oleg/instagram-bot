from threading import Thread
import json
import instaloader
from full_pipeline import *

def get_exit_flag():
    exit = True
    with open('exit_flag.json', 'r') as file:
        json_data = json.load(file)
        exit = json_data['exit']
    return exit


threads = []

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

for ruin in RUINS:
    thread = Thread(target=ruins_work, args=(ruin['username'], ruin['password'], ruin['proxy']))
    threads.append(thread)
for i in range(len(threads)):
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()