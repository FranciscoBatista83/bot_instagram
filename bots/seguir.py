import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import visitar_perfil, clicar_seguidores, rolar_ate_ultimo_seguidor, extrair_urls_seguidores, seguir_perfis
from core.file_manager import ler_urls_arquivo
from logger import log
from utils import pausa
import os
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para seguir perfis de seguidores de segundo nível do Instagram.")
    parser.add_argument("--user", required=True, help="Usuário do Instagram")
    parser.add_argument("--password", required=True, help="Senha do Instagram")
    parser.add_argument("--username", required=True, help="Username da conta logada")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password
    username_conta = args.username

    # Arquivo específico da conta
    arquivo_seguidores = f"seguidores_{username_conta}.txt"

    log.info(f"Iniciando o bot para seguir perfis de seguidores de segundo nível da conta @{username_conta}...")

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

        clicar_agora_nao(driver)

        urls_perfis_principais = ler_urls_arquivo(arquivo_seguidores)
        if not urls_perfis_principais:
            log.warning(f"Nenhuma URL de perfil principal encontrada em {arquivo_seguidores} para iniciar o processo.")
        else:
            log.info(f"Encontrados {len(urls_perfis_principais)} perfis principais para processar.")

            num_ciclos = 10
            log.info(f"O bot irá rodar por {num_ciclos} ciclos.")

            for ciclo_atual in range(1, num_ciclos + 1):
                log.info(f"=== INICIANDO CICLO {ciclo_atual}/{num_ciclos} ===")

                url_principal = random.choice(urls_perfis_principais)
                log.info(f"Perfil principal aleatório selecionado: {url_principal}")

                if not visitar_perfil(driver, url_principal):
                    log.warning(f"Não foi possível visitar o perfil principal: {url_principal}. Pulando para o próximo ciclo.")
                    continue

                if not clicar_seguidores(driver):
                    log.warning(f"Não foi possível acessar a lista de seguidores de {url_principal}. Pulando para o próximo ciclo.")
                    continue

                log.info(f"Iniciando processo de seguir 5 perfis de segundo nível de {url_principal}.")
                seguir_perfis(driver, lote=5, pausa_entre_lotes_min=20, pausa_entre_lotes_max=30)

                log.info(f"Ciclo {ciclo_atual} concluído. Aguardando próxima iteração.")
                if ciclo_atual < num_ciclos:
                    log.info(f"Pausa entre ciclos...")
                    pausa(min_tempo=20 * 60, max_tempo=30 * 60, jitter=0.5, nome="entre ciclos de seguir")

        log.info("Processo de seguir perfis de segundo nível concluído.")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
