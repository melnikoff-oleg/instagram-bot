# Instagram bot
Bot that follows friends of your friends on Instagram using proxy. It helps **get interested followers fast**

Get started:
1. pip install -r requirements.txt
2. Install Google Chrome web browser
3. Check your Chrome version via typing chrome://version in your browser
4. Download ChromeDriver from https://chromedriver.chromium.org/downloads, choose corresponding version
5. Put chromedriver file from downloaded ZIP-archive into project directory
6. Create following dirs/files in the project directory:
    - ff_calc/ff_all.txt - just empty file
    - people_followers/
    - proxyauth_plugin/
    - users/
7. Set up bot settings in config.py
8. Run create_user_json(username, password) method from full_pipeline.py on your new users, their JSON representation will be created, followers of added users will be added to the calculating pool, to calcalute their followers, and intersect them
9. Run all_threads.py it will start 3 pools of proccesses: finding followers of followers (FoF), calculating stats of FoF to know which of them we want to subscribe, selenium instances to subscribe via web browser. It will proccess 1 cycle of bot work, it will subscribe to 550 IG users, and unsubscribe from everyone who did not subscribe mutually
10. If you want repeat this cycle for some client, do this:
    - in user.py run methon full_restart(username)
    - in full_pipeline.py run method find_people(username)
    - run all_threads.py
    