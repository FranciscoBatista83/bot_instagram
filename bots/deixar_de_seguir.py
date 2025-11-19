import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import clicar_meu_perfil, clicar_seguindo, deixar_de_seguir_perfis
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para deixar de seguir perfis do Instagram.")
    parser.add_argument("--user", required=True, help="Usuário do Instagram")
    parser.add_argument("--password", required=True, help="Senha do Instagram")
    parser.add_argument("--username", required=True, help="Username da conta logada")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password
    username_conta = args.username

    # Carregar configurações do bot_configs.json
    config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")
    unfollow_batch_size = 10  # padrão
    unfollow_pause_min = 15  # 15 minutos padrão
    unfollow_pause_max = 30  # 30 minutos padrão

    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                configs = json.load(f)
            unfollow_batch_size = configs.get("unfollow_batch_size", 10)
            unfollow_pause_min = configs.get("unfollow_pause_min", 15)
            unfollow_pause_max = configs.get("unfollow_pause_max", 30)
            log.info(f"Configurações carregadas: lote={unfollow_batch_size}, pausa={unfollow_pause_min}-{unfollow_pause_max}min")
        except Exception as e:
            log.warning(f"Erro ao carregar configurações: {e}. Usando padrões.")
    else:
        log.warning("Arquivo bot_configs.json não encontrado. Usando configurações padrão.")

    log.info(f"Iniciando o bot para deixar de seguir perfis da conta @{username_conta}...")

    if not usuario or not senha:
        log.error("Credenciais não fornecidas. Por favor, use --user e --password.")
        sys.exit(1)

    driver = iniciar_driver()
    try:
        sucesso_login, username_logado = fazer_login(driver, usuario, senha)
        if not sucesso_login:
            log.error("Falha no login. Verifique as credenciais e tente novamente.")
            sys.exit(1)

        # Verificar se o username logado corresponde ao esperado
        if username_logado != username_conta:
            log.warning(f"Username logado ({username_logado}) diferente do esperado ({username_conta}). Usando {username_logado}.")
            username_conta = username_logado

        clicar_agora_nao(driver)

        if not clicar_meu_perfil(driver):
            log.error("Não foi possível acessar o perfil do usuário.")
            sys.exit(1)

        if not clicar_seguindo(driver):
            log.error("Não foi possível acessar a lista de 'seguindo'.")
            sys.exit(1)

        deixar_de_seguir_perfis(driver,
                              lote=unfollow_batch_size,
                              pausa_min=unfollow_pause_min,
                              pausa_max=unfollow_pause_max)

        log.info("Processo de deixar de seguir concluído.")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
