Automação OBI – Download dos “Cadernos de tarefas das provas” (Iniciação)

Script em Python que navega pelo portal da OBI e baixa apenas os PDFs cujo link começa com “Caderno de tarefas da prova” 
na modalidade Iniciação, cobrindo anos com fases normais (fase1, fase2, fase3) e anos com subfases (fase1A, fase1B, fase2A, fase2B).

✨ O que o script faz:

--> Acessa automaticamente as URLs de Iniciação para cada ano configurado.
--> Identifica os links de PDF cujo texto do link começa com Caderno de tarefas da prova.
--> Baixa os PDFs diretamente via requests (não abre o PDF no navegador).
--> Organiza os arquivos na estrutura:

Downloads_OBI/
  OBI2018/
    fase1/
    fase2/
    ...
  OBI2019/
  ...

🧰 Pré-requisitos

--> Python 3.9+ (Nesse código estou utilizando o Python Mais Atual "Python 3.13.2")
--> pip (Para baixar as Bibliotecas necessárias dentro do arquivo "requeriments.txt")
--> Firefox (o script usa Selenium + geckodriver; o webdriver_manager baixa o driver automaticamente)
--> Sistema testado em Windows (ajuste caminhos no base_download_dir se necessário).

🚀 Instalação
# 1) (opcional) criar e ativar venv no Windows
python -m venv AmbienteVirtual
AmbienteVirtual\Scripts\activate

# 2) instalar dependências
pip install selenium webdriver-manager requests

⚙️ Configuração

Edite no arquivo principal:

anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\seu.usuario\Downloads\Downloads_OBI"

- Ajuste anos conforme a necessidade.
- Troque base_download_dir para a sua pasta de destino.
- O script procura automaticamente por fase1, fase2, fase3 e, se não encontrar, tenta fase1A, fase1B (e o mesmo para fase2, fase3).

▶️ Execução:
python main.py

Exemplo de saída:

=== Baixando arquivos de OBI2018 - Iniciação ===
→ Encontrados 3 arquivos em https://olimpiada.ic.unicamp.br/passadas/OBI2018/fase1/iniciacao/
   ✅ Baixado: ProvaOBI2018_f1ij.pdf
   ✅ Baixado: ProvaOBI2018_f1ix.pdf
...

🧠 Como funciona (resumo técnico):

- Selenium (headless) abre cada URL de Iniciação por ano/fase.
- Coleta todos os <a href$='.pdf'> e filtra somente os cujo link.text começa com “Caderno de tarefas da prova”.
- Para cada PDF, faz download direto via requests.get() para a pasta adequada.

Esse desenho evita:
- Timeouts do geckodriver ao abrir PDFs no navegador,
- Problemas de salvar fora da pasta (o download é feito por código, não pelo Firefox).

📂 Estrutura do projeto
Automacao_OBI/
  main.py
  README.md
  AmbienteVirtual/        # (opcional) venv
  Downloads_OBI/          # destino dos PDFs

✅ Boas práticas

- Respeite o robots.txt e os termos do site.
- Evite cargas excessivas: não rode com paralelismo alto sem necessidade.
- Faça logs claros (o script já imprime ano/fase/URL/arquivo).