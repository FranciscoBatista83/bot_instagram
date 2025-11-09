import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import interagir_com_reels
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para curtir reels dos seguidores do Instagram.")
    parser.add_argument("--user", required=True, help="Usuário do Instagram")
    parser.add_argument("--password", required=True, help="Senha do Instagram")
    parser.add_argument("--username", required=True, help="Username da conta logada")
    parser.add_argument("--max_reels", type=int, default=None, help="Máximo de reels por perfil (0 = todos)")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password
    username_conta = args.username

    # Carregar configurações se não fornecidas via argumento
    max_reels = args.max_reels
    if max_reels is None:
        config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    configs = json.load(f)
                max_reels = configs.get("max_reels_per_profile", 3)
            except Exception as e:
                log.warning(f"Erro ao carregar configurações: {e}. Usando padrão 3.")
                max_reels = 3
        else:
            max_reels = 3

    # Arquivo específico da conta
    arquivo_seguidores = f"seguidores_{username_conta}.txt"

    log.info(f"Iniciando o bot para curtir reels dos seguidores da conta @{username_conta}...")

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
            arquivo_seguidores = f"seguidores_{username_conta}.txt"

        log.info(f"Usando arquivo: {arquivo_seguidores}")

        log.info("Verificando se há modal de salvar informações...")
        clicar_agora_nao(driver)

        log.info("Iniciando interação automática com reels de todos os perfis...")
        sucesso = interagir_com_reels(driver, arquivo_seguidores, max_reels)
        if sucesso:
            log.info("Interação com reels concluída com sucesso!")
        else:
            log.warning("Erro na interação com reels.")

        log.info("Processo de curtir reels concluído!")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
