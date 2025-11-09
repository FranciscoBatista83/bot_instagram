import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import clicar_meu_perfil, clicar_seguidores, rolar_ate_ultimo_seguidor, extrair_urls_seguidores
from core.file_manager import gerenciar_arquivo_urls, limpar_duplicatas_arquivo
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para acessar e coletar seguidores do Instagram.")
    parser.add_argument("--user", required=True, help="Usuário do Instagram")
    parser.add_argument("--password", required=True, help="Senha do Instagram")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password

    log.info("Iniciando o bot para acessar e coletar seguidores...")
    
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

        log.info("Tentando acessar o perfil do usuário...")
        if not clicar_meu_perfil(driver):
            log.error("Não foi possível acessar o perfil do usuário.")
            sys.exit(1)

        log.info("Tentando acessar a lista de seguidores...")
        if not clicar_seguidores(driver):
            log.error("Não foi possível acessar a lista de seguidores.")
            sys.exit(1)

        log.info("Fazendo scroll para carregar todos os seguidores...")
        rolar_ate_ultimo_seguidor(driver)

        log.info("Extraindo URLs dos seguidores e atualizando arquivo...")
        urls_encontradas = extrair_urls_seguidores(driver)

        if urls_encontradas:
            sucesso = gerenciar_arquivo_urls(urls_encontradas, "seguidores.txt")
            if sucesso:
                log.info("URLs dos seguidores salvas com sucesso!")
                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após limpeza duplicatas")
                log.info("Iniciando limpeza de duplicatas no arquivo...")
                limpeza_sucesso = limpar_duplicatas_arquivo("seguidores.txt")
                if limpeza_sucesso:
                    log.info("Limpeza de duplicatas concluída com sucesso!")
                else:
                    log.warning("Erro durante limpeza de duplicatas.")
            else:
                log.error("Erro ao salvar URLs dos seguidores.")
        else:
            log.warning("Nenhuma URL de seguidor encontrada.")

        log.info("Coleta de seguidores concluída!")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1) # Sair com erro
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
