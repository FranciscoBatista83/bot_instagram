import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
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
    args = parser.parse_args()

    usuario = args.user
    senha = args.password

    log.info("Iniciando o bot para deixar de seguir perfis...")
    
    if not usuario or not senha:
        log.error("Credenciais não fornecidas. Por favor, use --user e --password.")
        sys.exit(1) # Sair com erro

    driver = iniciar_driver()
    try:
        if not fazer_login(driver, usuario, senha):
            log.error("Falha no login. Verifique as credenciais e tente novamente.")
            sys.exit(1) # Sair com erro

        clicar_agora_nao(driver)
        
        if not clicar_meu_perfil(driver):
            log.error("Não foi possível acessar o perfil do usuário.")
            sys.exit(1)

        if not clicar_seguindo(driver):
            log.error("Não foi possível acessar a lista de 'seguindo'.")
            sys.exit(1)

        deixar_de_seguir_perfis(driver, lote=10)

        log.info("Processo de deixar de seguir concluído.")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1) # Sair com erro
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
