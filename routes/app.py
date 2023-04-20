from fastapi import APIRouter
from os import listdir as ld
import ssl
from os import path as pth
from config.db import conn
from notigram import ping
from fastapi.responses import HTMLResponse, FileResponse
from selenium.webdriver.chrome.service import Service
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bson import json_util
import time
import requests
from bs4 import BeautifulSoup

websites = [
    'https://repositorio.unam.mx/contenidos?f=883.%23.%23.a_lit:Repositorio%20de%20la%20Direcci%C3%B3n%20General%20de%20Bibliotecas%20y%20Servicios%20Digitales%20de%20Informaci%C3%B3n',
    'https://tesis.ipn.mx/handle/123456789/17534',
    'https://repositorio.tec.mx/discover',
    'http://zaloamati.azc.uam.mx/handle/11191/6701/discover'
]
prefs = {'download.default_directory': 'D:\Tesis\APIScrapp\documents'}
red = APIRouter()

def SearchUNAM(search):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 200)
    driver.get(websites[0])
    Cookies = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cc-btn")))
    Cookies.click()
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "input-search")))
    search_box.click()
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)
    array_docs = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.flex-wrap.details-rels-justify .doc-element-grid.card-rel.data-record-ind .do-grid-play.grid-main-img.select-record')))
    [(By.TAG_NAME, 'pre'), (By.TAG_NAME, 'body')]
    lista = 0
    for doc in array_docs:
        lista += 1
        doc.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'cont-completo'))).click()
        # Cambiar a la nueva ventana
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)
        # Obtener la URL de la nueva ventana
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "embed")))
        pdf_url = driver.current_url
        # Descargar el archivo PDF y guardar en un archivo local
        response = requests.get(pdf_url)
        with open(f"documents/UNAMdocumento{search}{lista}.pdf", "wb") as f:
            f.write(response.content)
        driver.close()
        wait.until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(driver.window_handles[0])
        wait.until(EC.visibility_of_element_located((By.ID, 'container_record_modal'))).send_keys(Keys.ESCAPE)
        if(lista == 5): break
    driver.quit()

def SearchIPN(search):
    driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_experimental_option('prefs', prefs))
    wait = WebDriverWait(driver, 200)
    driver.get(websites[1])
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "aspect_discovery_CommunitySearch_field_query")))
    search_box.click()
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)
    array_docs = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.ds-static-div.primary .ds-artifact-list .ds-artifact-item.clearfix.odd .thumbnail-wrapper')))
    array_docs[0].click()
    before = driver.current_url
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "img"))).click()
    after = driver.current_url
    if(before != after):
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "embed")))
        pdf_url = driver.current_url
        response = requests.get(pdf_url)
        with open(f"documents/IPNdocumento{search}.pdf", "wb") as f:
            f.write(response.content)
            while pth.exists('D:\Tesis\APIScrapp\documents\IPNdocumento{search}.pdf'):
                driver.quit()
    else:
        time.sleep(20)
    driver.quit()

def SearchTEC(search):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 2000)
    driver.get(websites[2])
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "aspect_discovery_SimpleSearch_field_query")))
    search_box.click()
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)
    array_docs = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.container .row.row-offcanvas.row-offcanvas-right .horizontal-slider.clearfix .col-xs-12.col-sm-12.col-md-9.main-content .ds-static-div.primary .ds-static-div.primary .row.ds-artifact-item .col-sm-3.hidden-xs .thumbnail.artifact-preview')))

    cont = 0
    listdocuments = []
    for doc in array_docs:
        doc.click()
        link = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe"))).get_attribute('src')
        evaluate = link[:30]
        if( 'repositorio.tec' in evaluate):
            listdocuments.append(link)
            cont +=1
        driver.back()
        if (cont == 5): break
    driver.quit()

    for i in listdocuments:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 2000)
        driver.get(i)
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "download")))
        search_box.click()
        time.sleep(7)
    driver.quit()

def SearchUAM(search):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 2000)
    driver.get(websites[3])
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "aspect_discovery_SimpleSearch_field_query")))
    search_box.click()
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)
    array_docs = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.container .row.row-offcanvas.row-offcanvas-right .horizontal-slider.clearfix .col-xs-12.col-sm-12.col-md-9.main-content .ds-static-div.primary .ds-static-div.primary .row.ds-artifact-item .col-sm-3.hidden-xs .thumbnail.artifact-preview')))

    cont = 0
    listdocuments = []
    for doc in array_docs:
        doc.click()
        link = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe"))).get_attribute('src')
        evaluate = link[:30]
        print(link)
        if( 'http://zaloamati.azc.uam.mx/th' in evaluate):
            listdocuments.append(link)
            cont +=1
        driver.back()
        if (cont == 5): break
    driver.quit()

    for i in listdocuments:
        prefs = {'download.default_directory': 'D:\Tesis\APIScrapp\documents'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 2000)
        driver.get(i)
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "download")))
        search_box.click()
        time.sleep(5)
    driver.quit()

def sendfiles():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        lista = ld('./documents')
        ids = []
        for i in range(len(lista)):
            with open(f'./documents/{lista[i]}', 'rb') as f:
                ids.append(str(conn.local.files.insert_one({
                    "name": lista[i],
                    "data": f.read()
                }).inserted_id))
        ids_str = ','.join(str(id_) for id_ in ids)
        URL = 'http://www.apicuttex-production.up.railway.app/document'
        serialized_ids = json_util.dumps(ids)
        print(serialized_ids)
        requests.post(URL, json={'ids': serialized_ids}, verify=ssl_context)
        return 'ok'
    except Exception as e:
        raise

@red.post('/test/${search}', response_model= list[str], tags=["Web Scrapping"])
def postText(search: str):
    # SearchUNAM(search)
    # SearchIPN(search)
    # SearchUAM(search)
    # SearchTEC(search)
    sendfiles()
    return 'ok'