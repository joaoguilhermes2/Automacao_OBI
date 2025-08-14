# Bibliotecas
import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

# Inicialização do Navegador
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Dados
anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\estagio.cop1\Downloads\Downloads_OBI"

def configurar_webdriver_firefox(download_dir):
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.animateNotifications", False)
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def esperar_download_terminar(download_dir):
    while True:
        time.sleep(1)
        # Verifica se existem arquivos temporários de download (.part)
        if not glob.glob(os.path.join(download_dir, "*.part")):
            break

def baixar_todos_links(driver, download_dir):
    # Captura todos os links de PDF
    links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")

    arquivos = []
    for link in links:
        if link.text.strip().startswith("Caderno de tarefas da prova"):
            arquivos.append(urljoin(driver.current_url, link.get_attribute("href")))
    
    print(f"→ Encontrados {len(arquivos)} arquivos.")
    
    for arquivo in arquivos:
        driver.get(arquivo)
        esperar_download_terminar(download_dir)

def baixar_iniciacao(ano):
    fases = ["fase1", "fase2", "fase3"]
    subfases = ["A", "B"]

    for fase in fases:
        url = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/"
        download_dir = os.path.join(base_download_dir, ano, fase)
        os.makedirs(download_dir, exist_ok=True)
        driver = configurar_webdriver_firefox(download_dir)
        driver.get(url)
        time.sleep(2)
        if "Not Found" not in driver.title:
            baixar_todos_links(driver, download_dir)
        else:
            for sub in subfases:
                url_sub = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}{sub}/iniciacao/"
                download_dir_sub = os.path.join(base_download_dir, ano, f"{fase}{sub}")
                os.makedirs(download_dir_sub, exist_ok=True)
                driver_sub = configurar_webdriver_firefox(download_dir_sub)
                driver_sub.get(url_sub)
                time.sleep(2)
                if "Not Found" not in driver_sub.title:
                    baixar_todos_links(driver_sub, download_dir_sub)
                driver_sub.quit()
        driver.quit()

# Loop principal
for ano in anos:
    try:
        print(f"\n=== Baixando arquivos de {ano} - Iniciação ===")
        driver = configurar_webdriver_firefox(base_download_dir)
        baixar_iniciacao(ano)
        driver.quit()
    except Exception as e:
        print(f"Erro ao baixar arquivos do {ano} - Iniciação: {e}")

print("\n✅ Todos os downloads concluídos!")