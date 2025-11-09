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
    parser.add_argument("--username", required=True, help="Username da conta logada")
    parser.add_argument("--max_followers", type=int, default=0, help="Número máximo de seguidores a extrair (0 = sem limite)")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password
    username_conta = args.username
    max_followers = args.max_followers

    # Arquivo específico da conta
    arquivo_seguidores = f"seguidores_{username_conta}.txt"

    log.info(f"Iniciando o bot para acessar e coletar seguidores da conta @{username_conta}...")

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

        # Aplicar limite máximo de seguidores se especificado
        if max_followers > 0 and urls_encontradas:
            urls_limitadas = urls_encontradas[:max_followers]
            log.info(f"Aplicando limite: {len(urls_encontradas)} seguidores encontrados, mantendo apenas os primeiros {max_followers}")
            urls_encontradas = urls_limitadas

        if urls_encontradas:
            sucesso = gerenciar_arquivo_urls(urls_encontradas, arquivo_seguidores)
            if sucesso:
                log.info(f"URLs dos seguidores salvas em {arquivo_seguidores}!")
                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após limpeza duplicatas")
                log.info("Iniciando limpeza de duplicatas no arquivo...")
                limpeza_sucesso = limpar_duplicatas_arquivo(arquivo_seguidores)
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
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
