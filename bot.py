from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from time import sleep
import random
import gender
import instaloader
from constants import *

def wait_rand_micro():
    sleep(random.randint(2, 7))

def wait_rand_short():
    sleep(random.randint(5, 30))

def wait_rand_mid():
    sleep(random.randint(300, 600))

def wait_rand_long():
    sleep(random.randint(1800, 3600))


def get_driver():
    def create_proxyauth_extension(proxy_host, proxy_port,
                                proxy_username, proxy_password,
                                scheme='http', plugin_path=None):
        """Proxy Auth Extension
        args:
            proxy_host (str): domain or ip address, ie proxy.domain.com
            proxy_port (int): port
            proxy_username (str): auth username
            proxy_password (str): auth password
        kwargs:
            scheme (str): proxy scheme, default http
            plugin_path (str): absolute path of the extension       
        return str -> plugin_path
        """
        import string
        import zipfile

        if plugin_path is None:
            plugin_path = 'proxyauth_plugin/vimm_chrome_proxyauth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_host=PROXY_DICT['host'],
        proxy_port=PROXY_DICT['port'],
        proxy_username=PROXY_DICT['username'],
        proxy_password=PROXY_DICT['password']
    )


    co = Options()
    #co.add_argument("--headless")
    co.add_argument("--start-maximized")
    co.add_extension(proxyauth_plugin_path)


    return webdriver.Chrome(chrome_options=co)

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.driver = get_driver()

    
    def login(self):
        self.driver.get(self.base_url + '/accounts/login/')
        sleep(3)
        try:
            self.driver.find_element_by_name('username').send_keys(self.username)
            self.driver.find_element_by_name('password').send_keys(self.password)
            self.driver.find_element_by_xpath("//div[contains(text(), 'Войти')]").click()
            sleep(3)
        except Exception as e:
            print(e)

    def exit(self):
        self.driver.get(self.base_url + '/' + self.username)
        sleep(3)
        try:
            settings_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button')
            settings_btn.click()
            sleep(3)
            self.driver.find_elements_by_xpath("//button[contains(text(), 'Выйти')]")[0].click()
            sleep(3)
            self.driver.find_elements_by_xpath("//button[contains(text(), 'Выйти')]")[0].click()
            sleep(3)
        except Exception as e:
            print(e)
    
    def nav_user(self, user):
        self.driver.get(self.base_url + '/' + user + '/')
        sleep(3)

    def follow_user(self, user):
        self.nav_user(user)
        self.driver.find_elements_by_xpath("//button[contains(text(), 'Подписаться')]")[0].click()
        sleep(3)
    
    def unfollow_user(self, user):
        self.nav_user(user)  
        try:
            btn = self.driver.find_element_by_class_name('glyphsSpriteFriend_Follow')
            btn.click()
        except Exception:
            btn = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')[0]
            if 'одписаться' in btn.get_attribute('innerHTML'):
                pass
            else:
                btn.click()
        sleep(2)
        self.driver.find_elements_by_xpath("//button[contains(text(), 'Отменить подписку')]")[0].click()
        sleep(2)
    
    def natural_subscribe(self, username):
        try:
            self.nav_user(username)
            sleep(3)
            try:
                self.driver.find_element_by_css_selector("#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div:nth-child(1)").click()
                sleep(3)
                self.driver.find_element_by_css_selector('svg._8-yf5[aria-label="Нравится"]').click()
                sleep(3)
            except Exception as e:
                print(e)
                print("Probably private account " + username)
            self.follow_user(username)
            print(username + " succesfully farmed by " + self.username)
        except Exception as e:
            print(username + " was NOT farmed by " + self.username)

    def natural_unsubscribe(self, username):
        try:
            self.nav_user(username)
            sleep(3)
            try:
                self.driver.find_element_by_css_selector("#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div:nth-child(1)").click()
                sleep(3)
            except Exception as e:
                print(e)
                print("No photos account " + username)
            self.unfollow_user(username)
            print(username + " succesfully antifarmed by " + self.username)
        except Exception as e:
            print(e)
            sleep(3)
            print(username + " was NOT antifarmed by " + self.username)
    
    def get_last_farmed(self):
        try:
            self.driver.get(self.base_url + '/accounts/activity')
            sleep(4)
            all = self.driver.find_elements_by_class_name('FPmhX')
            res = []
            for j in all:
                p = j.find_element_by_xpath('..')
                p = p.find_element_by_xpath('..')
                if 'подписался' in p.get_attribute('innerHTML'):
                    res.append(j.text)
            return res
        except Exception as e:
            print(e)
            return []

def save_html(driver):
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    with open('html_source_code.html', 'w', errors='ignore') as f:
        f.write(source_code)


if __name__ == '__main__':
    ig_bot = InstagramBot(USERNAME, PASSWORD)
    ig_bot.login()
    # sleep(3)
    # try:
    #     ig_bot.natural_subscribe('gromix.x')
    # except Exception as e:
    #     print(e)
    # ig_bot.driver.close()