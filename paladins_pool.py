from threading import Thread
import instaloader
from full_pipeline import *
from bot import *
threads = []

def get_exit_flag():
    exit = True
    with open('exit_flag.json', 'r') as file:
        json_data = json.load(file)
        exit = json_data['exit']
    return exit
    
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

for paladin_id, paladin in enumerate(PALADINS):
    thread = Thread(target=paladins_work, args=(paladin_id, paladin['proxy']))
    threads.append(thread)
for i in range(len(threads)):
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()