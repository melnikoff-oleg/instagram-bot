VPS = False # if deploying on VPS with Linux
HEADLESS = False # to run bot without explicit chrome window opening
DEBUG = False # debug mode
USE_PROXY = False # all operations would be done with corresponding proxies

# ig accounts to calculate followers of the client's followers, you can use proxy
RUINS = [{'username': 'ig_user_1_username', 'password': 'ig_user_1_password', 'proxy': {'host': '1.2.3.4', 'port': 12345, 'username': 'proxy_example_1_username', 'password': 'proxy_example_1_password'}}, {'username': 'ig_user_2_username', 'password': 'ig_user_2_password', 'proxy': {'host': '1.2.3.4', 'port': 12345, 'username': 'proxy_example_2_username', 'password': 'proxy_example_2_password'}}]

# ig accounts to calculate stats of followers of followers (FoF) to know which of them we want to subscribe
NOMADS = [{'username': 'ig_user_3_username', 'password': 'ig_user_3_password', 'proxy': {'host': '1.2.3.4', 'port': 12345, 'username': 'proxy_example_3_username', 'password': 'proxy_example_3_password'}}, {'username': 'ig_user_4_username', 'password': 'ig_user_4_password', 'proxy': {'host': '1.2.3.4', 'port': 12345, 'username': 'proxy_example_4_username', 'password': 'proxy_example_4_password'}}]

# if needed to use client's accounts via proxy
PALADINS = [{'proxy': {'host': '1.2.3.4', 'port': 12345, 'username': 'proxy_example_5_username', 'password': 'proxy_example_5_password'}}]

# you can leave these settings as they are
CLIENT_SLEEP_AFTER_BLOCKING = 46800

RUIN_BLOCK_SIZE = {True: 1, False: 5}
RUIN_SLEEP_TIME = {True: 5, False: 600}
FIND_PEOPLE_DEBUG = 2

NOMAD_BLOCK_SIZE = {True: 10, False: 50}
NOMAD_SLEEP_TIME = {True: 5, False: 600}
CALC_PEOPLE_DEBUG = 40

PALADIN_SLEEP_TIME = {True: 10, False: 3600}


TEST_USERNAME = 'example'
TEST_PASSWORD = 'example'
TEST_PROXY = {'host': '193.187.146.145', 'port': 8000, 'username': 'TMBmYc', 'password': 'Za5u2k'}


USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'

"""
User-Agents

Apple iPad
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4

Apple iPhone
Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1

Google Nexus
Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7

Samsung Galaxy Note 4
Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36

Samsung Galaxy Note 3
Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36
"""
