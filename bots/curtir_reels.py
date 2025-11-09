import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
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
    args = parser.parse_args()

    usuario = args.user
    senha = args.password

    log.info("Iniciando o bot para curtir reels dos seguidores...")
    
    if not usuario or not senha:
        log.error("Credenciais não fornecidas. Por favor, use --user e --password.")
        sys.exit(1) # Sair com erro

    driver = iniciar_driver()
    try:
        if not fazer_login(driver, usuario, senha):
            log.error("Falha no login. Verifique as credenciais e tente novamente.")
            sys.exit(1) # Sair com erro

        log.info("Verificando se há modal de salvar informações...")
        clicar_agora_nao(driver)

        log.info("Iniciando interação automática com reels de todos os perfis...")
        sucesso = interagir_com_reels(driver, "seguidores.txt")
        if sucesso:
            log.info("Interação com reels concluída com sucesso!")
        else:
            log.warning("Erro na interação com reels.")

        log.info("Processo de curtir reels concluído!")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1) # Sair com erro
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
