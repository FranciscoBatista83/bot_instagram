import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from utils import digitar_como_humano, pausa
from logger import log

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


def iniciar_driver():
    """Inicia o driver do Chrome com configurações otimizadas para automação."""
    log.info("Iniciando o driver do Chrome...")
    chrome_options = Options()
    arguments = ["--lang=pt-BR", "--start-maximized", "--incognito"]
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.prompt_for_download": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.automatic_downloads": 1,
        },
    )

    # Usar webdriver-manager para gerenciar automaticamente a versão correta do ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    log.info("Driver iniciado com sucesso.")
    return driver


def fazer_login(driver, usuario, senha):
    """Realiza o login no Instagram usando as credenciais fornecidas."""
    log.info("Navegando para a página de login do Instagram...")
    driver.get("https://www.instagram.com/")
    log.info("Página carregada. Aguardando elementos de login...")
    pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="carregar página login")

    wait = WebDriverWait(driver, 10)

    log.info("Procurando o campo de usuário...")
    campo_usuario = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    log.info("Campo de usuário encontrado. Preenchendo...")
    digitar_como_humano(campo_usuario, usuario)
    log.info("Usuário preenchido.")
    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após digitar usuário")

    log.info("Procurando o campo de senha...")
    campo_senha = driver.find_element(By.NAME, "password")
    log.info("Campo de senha encontrado. Preenchendo...")
    digitar_como_humano(campo_senha, senha)
    log.info("Senha preenchida.")
    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após digitar senha")

    log.info("Procurando o botão de login...")
    botao_login = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    log.info("Botão de login encontrado. Clicando...")
    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="antes clicar login")
    botao_login.click()
    
    # Verificar se o login foi bem-sucedido
    try:
        # Aguardar até que a URL mude para a página inicial ou um elemento pós-login apareça
        WebDriverWait(driver, 15).until(
            EC.url_contains("instagram.com/accounts/onetap/") or # Modal de salvar informações
            EC.url_contains("instagram.com/challenge/") or # Desafio de segurança
            EC.presence_of_element_located((By.XPATH, "//a[@href='/']//div[@role='link']")) # Ícone da home
        )
        log.info("Login aparentemente bem-sucedido ou redirecionado para verificação.")
        return True
    except Exception as e:
        log.error(f"Falha na verificação pós-login: {e}")
        return False
    finally:
        pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após clicar login")


def clicar_agora_nao(driver):
    """Clica no botão 'Agora não' do modal de salvar informações de login."""
    try:
        log.info("Verificando se o modal de salvar informações está presente...")
        # Aguardar um pouco para o modal aparecer (pausa humanizada)
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="aguardar modal login")

        # Tentar encontrar o botão "Agora não" de diferentes formas
        wait = WebDriverWait(driver, 5)

        # Método 1: Por texto exato
        try:
            botao_agora_nao = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(text(), 'Agora não')]")
                )
            )
            log.info("Botão 'Agora não' encontrado por texto. Clicando...")
            pausa(
                min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="antes clicar agora não"
            )
            botao_agora_nao.click()
            log.info("Botão 'Agora não' clicado com sucesso!")
            return True
        except:
            pass

        # Método 2: Por classes CSS baseadas no HTML fornecido
        try:
            # Procurar por elementos que contenham as classes características do botão
            elementos = driver.find_elements(
                By.CSS_SELECTOR, "[class*='x1e56ztr'] [class*='x1n2onr6']"
            )
            for elemento in elementos:
                if elemento.text.strip() == "Agora não":
                    log.info("Botão 'Agora não' encontrado por classe. Clicando...")
                    elemento.click()
                    log.info("Botão 'Agora não' clicado com sucesso!")
                    return True
        except:
            pass

        # Método 3: Por seletor mais amplo baseado na estrutura do modal
        try:
            # Procurar dentro do modal de salvar informações
            modal = driver.find_element(
                By.CSS_SELECTOR, "[class*='x14z9mp'][class*='x1lziwak']"
            )
            botoes = modal.find_elements(By.TAG_NAME, "div")
            for botao in botoes:
                if botao.text.strip() == "Agora não":
                    log.info("Botão 'Agora não' encontrado no modal. Clicando...")
                    botao.click()
                    log.info("Botão 'Agora não' clicado com sucesso!")
                    return True
        except:
            pass

        log.info("Modal de salvar informações não encontrado ou já foi fechado.")
        return False

    except Exception as e:
        log.warning(f"Erro ao tentar clicar no botão 'Agora não': {e}")
        return False
