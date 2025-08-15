#BIBLIOTECAS
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

# INICIALIZAÇÃO DO NAVEGADOR
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# IMPORTS
from Logger import configurar_logger

# Configura o logger
logger = configurar_logger()
logger.info("Automação - OBI iniciada.")

# Configurações
anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\estagio.cop1\Downloads\OBI\Automacao_OBI\Downloads_OBI"

def configurar_webdriver_firefox():
    logger.info("Configurando WebDriver Firefox (modo headless).")
    options = Options()
    options.headless = True  # Roda sem abrir janela
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def baixar_pdf(url, caminho_arquivo):
    try:
        resposta = requests.get(url, timeout=60)
        resposta.raise_for_status()
        with open(caminho_arquivo, "wb") as f:
            f.write(resposta.content)
        logger.info(f"Baixado: {os.path.basename(caminho_arquivo)}")
    except Exception as e:
        logger.error(f"Erro ao baixar {url}: {e}")

def baixar_todos_links(driver, download_dir):
    links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
    arquivos = [
        urljoin(driver.current_url, link.get_attribute("href"))
        for link in links if link.text.strip().startswith("Caderno de tarefas da prova")
    ]

    logger.info(f"--> Encontrados {len(arquivos)} arquivos em {driver.current_url}")

    for url in arquivos:
        nome_arquivo = os.path.basename(url)
        caminho_arquivo = os.path.join(download_dir, nome_arquivo)
        baixar_pdf(url, caminho_arquivo)

def baixar_iniciacao(ano):
    """Percorre as fases (normais e com A/B) e baixa PDFs de iniciação."""
    fases = ["fase1", "fase2", "fase3"]
    subfases = ["A", "B"]

    for fase in fases:
        try:
            # === Tratativa especial OBI2020 Fase 1 ===
            if ano == "OBI2020" and fase == "fase1":
                links_fase1_2020 = {
                    "Turno A": "https://olimpiada.ic.unicamp.br/passadas/OBI2020/fase1/iniciacao-a/",
                    "Turno B": "https://olimpiada.ic.unicamp.br/passadas/OBI2020/fase1/iniciacao-b/"
                }
                for turno, link in links_fase1_2020.items():
                    pasta_turno = os.path.join(base_download_dir, ano, fase, turno)
                    os.makedirs(pasta_turno, exist_ok=True)
                    logger.info(f"Acessando {link} ({turno})")

                    driver = configurar_webdriver_firefox()
                    driver.get(link)
                    time.sleep(2)

                    if "Not Found" not in driver.page_source:
                        logger.info(f"Página encontrada para {fase} {turno} de {ano}.")
                        baixar_todos_links(driver, pasta_turno)
                    else:
                        logger.warning(f"Página não encontrada para {fase} {turno} de {ano}.")

                    driver.quit()
                continue  # Pula para a próxima fase

            # === Fluxo normal para OBI2024 ou outros anos ===
            if ano == "OBI2024":
                url_fase = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/cadernos/"
                pasta_fase = os.path.join(base_download_dir, ano, fase)
                os.makedirs(pasta_fase, exist_ok=True)
                logger.info(f"Acessando URL especial para OBI2024: {url_fase}")

                driver = configurar_webdriver_firefox()
                driver.get(url_fase)
                time.sleep(2)

                if "Not Found" not in driver.page_source:
                    logger.info(f"Página encontrada para {fase} de {ano}.")
                    baixar_todos_links(driver, pasta_fase)
                else:
                    logger.warning(f"Página não encontrada para {fase} de {ano}.")
                
                driver.quit()
                continue

            # === Fluxo normal para outros anos ===
            url_fase = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/"
            pasta_fase = os.path.join(base_download_dir, ano, fase)
            os.makedirs(pasta_fase, exist_ok=True)
            logger.info(f"Acessando {url_fase}")

            driver = configurar_webdriver_firefox()
            driver.get(url_fase)
            time.sleep(2)

            if "Not Found" not in driver.page_source:
                logger.info(f"Página encontrada para {fase} de {ano}.")
                baixar_todos_links(driver, pasta_fase)
                driver.quit()
                continue

            logger.warning(f"Página não encontrada para {fase} de {ano}. Tentando subfases...")
            driver.quit()

            # Se a fase normal não existe, tenta subfases A e B
            for sub in subfases:
                try:
                    url_sub = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}{sub}/iniciacao/"
                    pasta_sub = os.path.join(base_download_dir, ano, f"{fase}{sub}")
                    os.makedirs(pasta_sub, exist_ok=True)
                    logger.info(f"Acessando subfase {fase}{sub}: {url_sub}")

                    driver_sub = configurar_webdriver_firefox()
                    driver_sub.get(url_sub)
                    time.sleep(2)

                    if "Not Found" not in driver_sub.page_source:
                        logger.info(f"Página encontrada para subfase {fase}{sub} de {ano}.")
                        baixar_todos_links(driver_sub, pasta_sub)
                    else:
                        logger.warning(f"Subfase {fase}{sub} não encontrada para {ano}.")

                    driver_sub.quit()
                except Exception as e:
                    logger.error(f"Erro na subfase {fase}{sub} do ano {ano}: {e}")

        except Exception as e:
            logger.error(f"Erro na fase {fase} do ano {ano}: {e}")

# Loop principal
for ano in anos:
    logger.info(f"\nBaixando arquivos de {ano} - Iniciação ===")
    try:
        baixar_iniciacao(ano)
    except Exception as e:
        logger.error(f"Erro geral no ano {ano}: {e}")

logger.info("\nTodos os downloads concluídos!")