import os
import time
import glob
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Configurações
anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\estagio.cop1\Downloads\Downloads_OBI"

def configurar_webdriver_firefox():
    """Configura e retorna o WebDriver Firefox (sem precisar configurar download)."""
    options = Options()
    options.headless = True  # Roda sem abrir janela
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def baixar_pdf(url, caminho_arquivo):
    """Baixa o PDF diretamente usando requests."""
    try:
        resposta = requests.get(url, timeout=60)
        resposta.raise_for_status()
        with open(caminho_arquivo, "wb") as f:
            f.write(resposta.content)
        print(f"   ✅ Baixado: {os.path.basename(caminho_arquivo)}")
    except Exception as e:
        print(f"   ⚠ Erro ao baixar {url}: {e}")

def baixar_todos_links(driver, download_dir):
    """Captura os PDFs cujo texto começa com 'Caderno de tarefas da prova' e baixa direto."""
    links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
    arquivos = [
        urljoin(driver.current_url, link.get_attribute("href"))
        for link in links if link.text.strip().startswith("Caderno de tarefas da prova")
    ]

    print(f"→ Encontrados {len(arquivos)} arquivos em {driver.current_url}")

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
            # Tenta fase normal
            url_fase = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/"
            pasta_fase = os.path.join(base_download_dir, ano, fase)
            os.makedirs(pasta_fase, exist_ok=True)

            driver = configurar_webdriver_firefox()
            driver.get(url_fase)
            time.sleep(2)

            if "Not Found" not in driver.page_source:
                baixar_todos_links(driver, pasta_fase)
                driver.quit()
                continue  # Vai para próxima fase

            driver.quit()

            # Se a fase normal não existe, tenta subfases A e B
            for sub in subfases:
                try:
                    url_sub = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}{sub}/iniciacao/"
                    pasta_sub = os.path.join(base_download_dir, ano, f"{fase}{sub}")
                    os.makedirs(pasta_sub, exist_ok=True)

                    driver_sub = configurar_webdriver_firefox()
                    driver_sub.get(url_sub)
                    time.sleep(2)

                    if "Not Found" not in driver_sub.page_source:
                        baixar_todos_links(driver_sub, pasta_sub)

                    driver_sub.quit()
                except Exception as e:
                    print(f"⚠ Erro na subfase {fase}{sub} do ano {ano}: {e}")

        except Exception as e:
            print(f"⚠ Erro na fase {fase} do ano {ano}: {e}")

# Loop principal
for ano in anos:
    print(f"\n=== Baixando arquivos de {ano} - Iniciação ===")
    try:
        baixar_iniciacao(ano)
    except Exception as e:
        print(f"⚠ Erro geral no ano {ano}: {e}")

print("\n✅ Todos os downloads concluídos!")
