# Bibliotecas
import os
import time

# Inicialização do Navegador
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = "C:/meus_arquivos_baixados"

def configurar_webdriver_firefox(download_dir):
    options = Options()
    options.binary_location = r"C:\Users\JoãoSampaio\AppData\Local\Mozilla Firefox\firefox.exe"  # coloque o caminho correto
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("pdfjs.disabled", True)  # impede visualização de PDFs
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.animateNotifications", False)

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def baixar_obi_padrao(driver, ano):
    url = f"https://olimpiada.ic.unicamp.br/passadas/{ano.lower()}"
    driver.get(url)
    time.sleep(5)

def baixar_obi2020(driver):
    url = f"https://olimpiada.ic.unicamp.br/passadas/obi2020"
    driver.get(url)
    time.sleep(5)


for ano in anos:
    try:
        # Cria pasta específica para o ano
        download_dir = os.path.join(base_download_dir, ano)
        os.makedirs(download_dir, exist_ok=True)

        driver = configurar_webdriver_firefox(download_dir)

        if ano == "OBI2020":
            baixar_obi2020(driver)
        else:
            baixar_obi_padrao(driver, ano)

    except Exception as e:
        print(f"Erro ao baixar arquivos do {ano}: {e}")