import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

# ==========================================
# CONFIGURAÇÕES
# ==========================================

USUARIO = "julio@techsistemas.com.br"
SENHA = "87126155JoaoG"
URL = "https://livesistemas.bitrix24.com.br/crm/deal/kanban/category/21/"

REVENDAS = {
    "jsoft": "JFOST",
    "live": "Growth Live",
    "mg": "GRUPO AUTOMAÇÃO",
    "sa": "SA TECNOLOGIA & SISTEMAS",
    "ms": "MSRCARD",
    "jet": "JET SPED TECNOLOGIA",
    "dmoneito": "DMONTEIRO INFO",
    "alter": "ALTERNATIVA FOZ",
    "soph": "SOPHTECH INFORMATICA",
    "age": "AGEDATA",
    "centro": "CENTRÔNICS AUTOMAÇÃO",
    "dyna": "DYNATEK",
}

# ==========================================
# LOG
# ==========================================

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    app.update()

# ==========================================
# EXTRAÇÃO INTELIGENTE
# ==========================================

def extrair_empresa_e_revenda(titulo_completo):

    if not titulo_completo.strip():
        raise Exception("Título retornou vazio.")

    titulo = titulo_completo.upper()
    titulo = titulo.replace("ATENDIMENTO DE PLANTÃO", "")
    titulo = titulo.replace(" - ", " ")
    titulo = titulo.strip()

    palavras = titulo.split()

    if len(palavras) < 2:
        raise Exception("Título fora do padrão esperado.")

    codigo = palavras[-1].lower()

    if codigo not in REVENDAS:
        raise Exception(f"Sigla não reconhecida: {codigo}")

    empresa = " ".join(palavras[:-1]).strip()

    return empresa.title(), REVENDAS[codigo]

# ==========================================
# LOGIN
# ==========================================

def realizar_login(driver):

    wait = WebDriverWait(driver, 40)

    wait.until(EC.presence_of_element_located((By.ID, "login"))).send_keys(USUARIO)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continuar')]"))).click()

    time.sleep(2)

    driver.switch_to.active_element.send_keys(SENHA)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continuar')]"))).click()

    wait.until(EC.url_contains("/crm"))

    log("Login realizado.")
    time.sleep(10)

# ==========================================
# SCROLL LATERAL
# ==========================================

def scroll_ate_final_kanban(driver):

    try:
        wait = WebDriverWait(driver, 20)
        seta = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main-kanban-ear-right")))

        ActionChains(driver).move_to_element(seta).perform()

        WebDriverWait(driver, 60).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "main-kanban-ear-right"))
        )

        log("Scroll lateral concluído.")

    except:
        log("Já estava no final.")

# ==========================================
# LOCALIZAR COLUNA
# ==========================================

def localizar_coluna_plantao(driver):

    colunas = driver.find_elements(By.XPATH, "//div[contains(@class,'main-kanban-column')]")

    for coluna in colunas:
        try:
            titulo = coluna.find_element(
                By.XPATH,
                ".//div[contains(@class,'main-kanban-column-title')]"
            ).text

            if "PLANTÃO" in titulo.upper():
                log("Coluna Plantão encontrada.")
                return coluna
        except:
            continue

    return None

# ==========================================
# AUTOMAÇÃO
# ==========================================

def executar_automacao():

    try:
        log("Iniciando navegador...")

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, 30)

        driver.get(URL)

        realizar_login(driver)
        scroll_ate_final_kanban(driver)

        total = 0

        while True:

            coluna = localizar_coluna_plantao(driver)
            cards = coluna.find_elements(By.XPATH, ".//div[contains(@class,'crm-kanban-item')]")

            if not cards:
                log("Nenhum card restante.")
                break

            card = cards[0]

            titulo_elemento = card.find_element(By.CLASS_NAME, "crm-kanban-item-title")
            driver.execute_script("arguments[0].scrollIntoView();", titulo_elemento)
            time.sleep(1)
            titulo_elemento.click()

            log("Card aberto.")
            time.sleep(3)

            # Captura título real
            wait.until(EC.visibility_of_element_located((By.ID, "pagetitle")))
            titulo_real = driver.find_element(By.ID, "pagetitle").text.strip()

            log(f"Título capturado: {titulo_real}")

            empresa, revenda = extrair_empresa_e_revenda(titulo_real)

            log(f"Empresa: {empresa}")
            log(f"Revenda: {revenda}")

            # ==========================
            # FECHAR CHAMADOS
            # ==========================

            wait.until(EC.element_to_be_clickable((By.ID, "C21:WON"))).click()
            log("Fechar chamados clicado.")

            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Chamados Concluídos')]"))).click()
            time.sleep(1)

            # Campo Revenda
            wait.until(EC.element_to_be_clickable((
                By.ID, "ui-tile-selector-uf-crm-1718155544cODy3K1771182003"
            ))).send_keys(revenda)

            time.sleep(1)

            # Campo Empresa
            wait.until(EC.element_to_be_clickable((
                By.ID, "ui-tile-selector-uf-crm-1718208547mgm7hR1771182003"
            ))).send_keys(empresa)

            time.sleep(1)

            # Salvar
            wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, "ui-btn-primary"
            ))).click()

            log("Salvo.")
            time.sleep(2)

            # Fechar painel lateral
            wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, "side-panel-label-icon-close"
            ))).click()

            log("Painel fechado.")
            time.sleep(2)

            total += 1
            progress_bar["value"] = total
            app.update()

        log("Processo finalizado com sucesso.")

    except Exception as e:
        log(f"ERRO: {str(e)}")
        messagebox.showerror("Erro", str(e))

# ==========================================
# THREAD
# ==========================================

def iniciar_thread():
    threading.Thread(target=executar_automacao).start()

# ==========================================
# INTERFACE
# ==========================================

app = tk.Tk()
app.title("Bot Fechamento Plantão")
app.geometry("600x500")

progress_bar = ttk.Progressbar(app, length=400)
progress_bar.pack(pady=10)

tk.Button(
    app,
    text="Iniciar Fechamento",
    command=iniciar_thread,
    bg="green",
    fg="white"
).pack(pady=10)

log_text = tk.Text(app, height=20, width=70)
log_text.pack()

app.mainloop()
