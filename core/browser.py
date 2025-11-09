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


def extrair_username_logado(driver):
    """Extrai o username da conta atualmente logada."""
    try:
        log.info("Extraindo username da conta logada...")
        wait = WebDriverWait(driver, 10)

        # Método 1: Procurar pelo link do perfil no header/topo
        try:
            # Aguardar um pouco para a página carregar completamente
            import time
            time.sleep(2)

            # Procurar por links que contenham o username no header
            header_links = driver.find_elements(By.CSS_SELECTOR, "header a[href^='/']")
            for link in header_links:
                href = link.get_attribute("href")
                if href and href.startswith("https://www.instagram.com/"):
                    username = href.replace("https://www.instagram.com/", "").rstrip("/")
                    # Validar que é um username válido (não contém caracteres especiais de URL)
                    if (username and
                        len(username) >= 3 and
                        len(username) <= 30 and
                        username.replace("_", "").replace(".", "").isalnum() and
                        not username.startswith("explore") and
                        not username.startswith("reels") and
                        not username.startswith("direct") and
                        not "?" in username and
                        not "%" in username):
                        log.info(f"Username extraído: {username}")
                        return username
        except Exception as e:
            log.warning(f"Erro no método 1: {e}")

        # Método 2: Procurar na barra lateral ou menu
        try:
            sidebar_links = driver.find_elements(By.CSS_SELECTOR, "nav a[href^='/']")
            for link in sidebar_links:
                href = link.get_attribute("href")
                if href and href.startswith("https://www.instagram.com/"):
                    username = href.replace("https://www.instagram.com/", "").rstrip("/")
                    if (username and
                        len(username) >= 3 and
                        len(username) <= 30 and
                        username.replace("_", "").replace(".", "").isalnum() and
                        not username.startswith("explore") and
                        not username.startswith("reels") and
                        not username.startswith("direct") and
                        not "?" in username and
                        not "%" in username):
                        log.info(f"Username extraído (método 2): {username}")
                        return username
        except Exception as e:
            log.warning(f"Erro no método 2: {e}")

        # Método 3: Procurar por elementos com data-testid ou aria-label específicos
        try:
            profile_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='user-avatar'], [aria-label*='Seu perfil']")
            for element in profile_elements:
                # Procurar por links próximos
                parent = element
                for _ in range(3):  # Subir até 3 níveis
                    parent = parent.find_element(By.XPATH, "..")
                    links = parent.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        href = link.get_attribute("href")
                        if href and href.startswith("https://www.instagram.com/"):
                            username = href.replace("https://www.instagram.com/", "").rstrip("/")
                            if (username and
                                len(username) >= 3 and
                                len(username) <= 30 and
                                username.replace("_", "").replace(".", "").isalnum() and
                                not username.startswith("explore") and
                                not username.startswith("reels") and
                                not username.startswith("direct") and
                                not "?" in username and
                                not "%" in username):
                                log.info(f"Username extraído (método 3): {username}")
                                return username
        except Exception as e:
            log.warning(f"Erro no método 3: {e}")

        # Método 4: Fallback - tentar encontrar por meta tags ou title
        try:
            title = driver.title
            if "@" in title:
                username = title.split("@")[1].split(" ")[0].strip("()")
                if username and len(username) >= 3:
                    log.info(f"Username extraído do título (método 4): {username}")
                    return username
        except Exception as e:
            log.warning(f"Erro no método 4: {e}")

        log.warning("Não foi possível extrair username automaticamente")
        return None

    except Exception as e:
        log.error(f"Erro ao extrair username: {e}")
        return None


def fazer_login(driver, usuario, senha):
    """Realiza o login no Instagram usando as credenciais fornecidas.

    Returns:
        tuple: (sucesso: bool, username: str or None)
    """
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

        # Extrair o username da conta logada
        username_logado = extrair_username_logado(driver)
        if username_logado:
            log.info(f"Conta logada: {username_logado}")
            return True, username_logado
        else:
            log.warning("Login bem-sucedido, mas não foi possível extrair o username")
            return True, usuario  # Fallback: usar o username fornecido

    except Exception as e:
        log.error(f"Falha na verificação pós-login: {e}")
        return False, None
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
