import os
import time
import requests
import random
import datetime
from unicodedata import normalize
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def main():
    driver = initDriver()
    img = getImage(driver)
    downloadImage(img)
    login(driver)
    disablePopUp(driver)
    time.sleep(1)
    openContact(driver)
    time.sleep(1)
    sendFile(driver)
    time.sleep(3)

def initDriver():
    driver = webdriver.Chrome()
    return driver

def getImage(driver):
    driver.get(f'https://www.imagensdiarias.com.br/search?q={getDayOfWeek()}')
    imagens = driver.find_elements("css selector", ".post img")
    lenImages = len(imagens)

    if lenImages > 0:
        randomImage = random.choice(imagens)
        randomImage = randomImage.get_attribute('src')
        return randomImage
    else:
        print("Sem imagens.")
    
    return None
    
def downloadImage(imageUrl):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        with open('image.jpg', 'wb') as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")

def getDayOfWeek():
    dias_semana = ("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo")
    hoje = datetime.date.today()
    numero_dia = hoje.weekday()
    nome_dia = dias_semana[numero_dia]
    nome_dia_normalizado = normalize('NFKD', nome_dia).encode('ASCII', 'ignore').decode('ASCII')
    return nome_dia_normalizado

def login(driver):
    driver.get('https://web.whatsapp.com/')
    
    # Espera até que o elemento canvas apareça na página
    canvas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas"))
    )
    #espera até que a pagina seja modificada, se for modificado fecha o navegador
    driver.implicitly_wait(10)
    if canvas.is_displayed():
        print("Por Favor escaneie o QR Code com seu celular...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".xk50ysn.x14ug900.x1603h9y.xgif2c7"))
        )
        print("Login realizado com sucesso.")
        
def disablePopUp(driver):        
    time.sleep(3)
    
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()

def openContact(driver):
    contato = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".x10l6tqk.xh8yej3.x1g42fcv"))
    )
    contato.click()

def sendFile(driver):
    attach_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span[data-icon='plus-rounded']")
        )
    )
    attach_button.click()

    image_path = os.path.abspath("image.jpg") 

    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        )
    )
    file_input.send_keys(image_path) 
    time.sleep(2)

    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "span[data-icon='wds-ic-send-filled']")
            )
    )
    send_button.click()

if __name__ == "__main__":
    main()