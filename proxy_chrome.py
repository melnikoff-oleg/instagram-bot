from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from time import sleep
import random
import gender
import instaloader
from config import *


def get_driver(proxy):
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
        proxy_host=proxy['host'],
        proxy_port=proxy['port'],
        proxy_username=proxy['username'],
        proxy_password=proxy['password']
    )


    co = Options()
    co.add_argument('--user-agent="{}"'.format(USER_AGENT))
    # to disable geolocation in browser. maybe Instagram don't like this
    # prefs = {'profile.default_content_setting_values.geolocation': 2}
    # co.add_experimental_option('prefs',prefs)
    if VPS:
        co.add_argument('--no-sandbox')
    if VPS or USE_PROXY:
        co.add_argument("--start-maximized")
        co.add_extension(proxyauth_plugin_path)
    if HEADLESS and not VPS:
        co.add_argument("--headless")

    if VPS:
        driver = webdriver.Chrome(executable_path='./drivers/chromedriver', options=co)
    else:
        driver = webdriver.Chrome(chrome_options=co)

    return driver



if __name__ == '__main__':
    pass
    # proxy = {'host': 'example', 'port': 12345, 'username': 'example', 'password': 'example'}
    # driver = get_driver(proxy)
    # driver.get('https://httpbin.org/ip')