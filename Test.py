from fastapi import APIRouter
from os import environ as env
from notigram import ping
from fastapi.responses import HTMLResponse, FileResponse
from selenium.webdriver.chrome.service import Service
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import time
import requests
from bs4 import BeautifulSoup


websites = [
    'http://zaloamati.azc.uam.mx/themes/Mirage2/vendor/pdfjs/web/viewer.html?file=/bitstream/handle/11191/761/Fresnillo_monografia.pdf'
]


def test():
    prefs = {'download.default_directory': 'D:\Tesis\APIScrapp\documents'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20000)
    driver.get(websites[0])
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "download")))
    search_box.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "embed")))

test()