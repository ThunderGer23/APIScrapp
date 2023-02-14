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
    'https://repositorio.unam.mx/contenidos?f=883.%23.%23.a_lit:Repositorio%20de%20la%20Direcci%C3%B3n%20General%20de%20Bibliotecas%20y%20Servicios%20Digitales%20de%20Informaci%C3%B3n'
]

red = APIRouter()

def OpenWebSite():
    driver = webdriver.Chrome(executable_path='/chromedriver.exe')
    driver.get(websites[0])
    search_box = driver.find_element_by_id("input-search")
    search_box.send_keys("PNL")
    search_box.send_keys(Keys.RETURN)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, "btn-general-buscar")))
    element.click()
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "element-ing-data-record")))
    element.click()
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cont-completo")))
    element.click()
    # Cambiar a la nueva ventana
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    # Obtener la URL de la nueva ventana
    pdf_url = driver.current_url
    # Descargar el archivo PDF y guardar en un archivo local
    response = requests.get(pdf_url)
    with open("documento.pdf", "wb") as f:
        f.write(response.content)
    time.sleep(5)  # Espera 5 segundos para que la página cargue completamente
    html = driver.page_source
    driver.quit()
    return FileResponse("documento.pdf")


@red.post('/test', response_model= list[str], tags=["Cod"])
def postText():
    OpenWebSite()