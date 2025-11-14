import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
import json
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

    # Carregar configurações do bot_configs.json
    config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")
    follow_batch_size = 5  # padrão
    follow_pause_min = 20  # 20 minutos padrão
    follow_pause_max = 30  # 30 minutos padrão
    follow_cycles = 10  # 10 ciclos padrão

    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                configs = json.load(f)
            follow_batch_size = configs.get("follow_batch_size", 5)
            follow_pause_min = configs.get("follow_pause_min", 20)
            follow_pause_max = configs.get("follow_pause_max", 30)
            follow_cycles = configs.get("follow_cycles", 10)
            log.info(f"Configurações carregadas: lote={follow_batch_size}, pausa={follow_pause_min}-{follow_pause_max}min, ciclos={follow_cycles}")
        except Exception as e:
            log.warning(f"Erro ao carregar configurações: {e}. Usando padrões.")
    else:
        log.warning("Arquivo bot_configs.json não encontrado. Usando configurações padrão.")

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

            log.info(f"O bot irá rodar por {follow_cycles} ciclos.")

            for ciclo_atual in range(1, follow_cycles + 1):
                log.info(f"=== INICIANDO CICLO {ciclo_atual}/{follow_cycles} ===")

                url_principal = random.choice(urls_perfis_principais)
                log.info(f"Perfil principal aleatório selecionado: {url_principal}")

                if not visitar_perfil(driver, url_principal):
                    log.warning(f"Não foi possível visitar o perfil principal: {url_principal}. Pulando para o próximo ciclo.")
                    continue

                if not clicar_seguidores(driver):
                    log.warning(f"Não foi possível acessar a lista de seguidores de {url_principal}. Pulando para o próximo ciclo.")
                    continue

                log.info(f"Iniciando processo de seguir {follow_batch_size} perfis de segundo nível de {url_principal}.")
                seguir_perfis(driver, lote=follow_batch_size, pausa_entre_lotes_min=follow_pause_min, pausa_entre_lotes_max=follow_pause_max)

                log.info(f"Ciclo {ciclo_atual} concluído. Aguardando próxima iteração.")
                if ciclo_atual < follow_cycles:
                    log.info(f"Pausa entre ciclos...")
                    pausa(min_tempo=follow_pause_min * 60, max_tempo=follow_pause_max * 60, jitter=0.5, nome="entre ciclos de seguir")

        log.info("Processo de seguir perfis de segundo nível concluído.")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
