import sys
import os
import argparse # Importar argparse para lidar com argumentos de linha de comando
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.keys import Keys
from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import interagir_com_reels, encontrar_reels_perfil, curtir_reel
from logger import log
from utils import pausa
import os


def curtir_reels_perfil(driver, max_reels=3):
    """Curte múltiplos reels de um perfil específico.

    Args:
        driver: Instância do webdriver
        max_reels: Número máximo de reels a curtir por perfil

    Returns:
        int: Número de reels efetivamente curtidos
    """
    try:
        log.info(f"Procurando ate {max_reels} reels neste perfil...")

        # Encontrar reels disponíveis no perfil
        reels_encontrados = encontrar_reels_perfil(driver, max_reels)

        if not reels_encontrados:
            log.info("Nenhum reel encontrado neste perfil.")
            return 0

        log.info(f"Encontrados {len(reels_encontrados)} reels. Curtindo ate {max_reels}...")

        reels_curtidos = 0

        # Curtir cada reel encontrado (até o limite)
        for i, reel in enumerate(reels_encontrados[:max_reels]):
            try:
                log.info(f"Clicando no reel {i+1}/{min(max_reels, len(reels_encontrados))}")

                # Clicar no reel
                reel.click()
                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="abrir reel")

                # Tentar curtir o reel
                if curtir_reel(driver):
                    reels_curtidos += 1
                    log.info(f"Reel {i+1} curtido com sucesso!")
                else:
                    log.info(f"Reel {i+1} ja estava curtido ou nao foi possivel curtir.")

                # Voltar para o perfil (fechar o reel)
                try:
                    # Tentar clicar no X ou usar ESC
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    pausa(min_tempo=0.5, max_tempo=1.0, jitter=0.1, nome="fechar reel")
                except:
                    # Fallback: recarregar a página do perfil
                    driver.back()
                    pausa(min_tempo=2, max_tempo=4, jitter=0.3, nome="recarregar perfil")

                # Pequena pausa entre reels
                if i < len(reels_encontrados[:max_reels]) - 1:
                    pausa(min_tempo=1, max_tempo=2, jitter=0.2, nome="entre reels")

            except Exception as e:
                log.warning(f"Erro ao processar reel {i+1}: {e}")
                continue

        log.info(f"Total: {reels_curtidos} reels curtidos neste perfil.")
        return reels_curtidos

    except Exception as e:
        log.error(f"Erro geral ao curtir reels do perfil: {e}")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot para curtir reels dos seguidores do Instagram.")
    parser.add_argument("--user", required=True, help="Usuário do Instagram")
    parser.add_argument("--password", required=True, help="Senha do Instagram")
    parser.add_argument("--username", required=True, help="Username da conta logada")
    args = parser.parse_args()

    usuario = args.user
    senha = args.password
    username_conta = args.username

    # Carregar configurações do bot_configs.json
    config_file = os.path.join(os.path.dirname(__file__), "..", "bot_configs.json")
    reels_per_profile = 3  # padrão
    pause_min_profiles = 10  # padrão 10 segundos
    pause_max_profiles = 30  # padrão 30 segundos

    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                configs = json.load(f)
            reels_per_profile = configs.get("reels_per_profile", 3)
            pause_min_profiles = configs.get("pause_min_profiles", 10)
            pause_max_profiles = configs.get("pause_max_profiles", 30)
            log.info(f"Configurações carregadas: {reels_per_profile} reels por perfil, pausa {pause_min_profiles}-{pause_max_profiles}s entre perfis")
        except Exception as e:
            log.warning(f"Erro ao carregar configurações: {e}. Usando padrões.")
    else:
        log.warning("Arquivo bot_configs.json não encontrado. Usando configurações padrão.")

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

        log.info("Iniciando interação automática com reels em loop infinito...")

        # Importar função para ler URLs do arquivo
        from core.file_manager import ler_urls_arquivo
        import random

        perfis_processados = 0
        reels_curtidos_total = 0

        while True:  # Loop infinito
            try:
                # Ler perfis disponíveis
                urls_perfis = ler_urls_arquivo(arquivo_seguidores)
                if not urls_perfis:
                    log.warning("Nenhum perfil encontrado no arquivo. Aguardando 60 segundos...")
                    pausa(min_tempo=60, max_tempo=60, jitter=0, nome="aguardar perfis")
                    continue

                # Escolher perfil aleatório
                url_perfil = random.choice(urls_perfis)
                perfis_processados += 1

                log.info(f"Processando perfil {perfis_processados}: {url_perfil}")

                # Navegar para o perfil
                driver.get(url_perfil)
                pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="carregar perfil")

                # Tentar encontrar e curtir reels
                reels_curtidos = curtir_reels_perfil(driver, reels_per_profile)
                reels_curtidos_total += reels_curtidos

                log.info(f"Status: {reels_curtidos} reels curtidos neste perfil (total: {reels_curtidos_total})")

                # Pausa configurável entre perfis
                log.info(f"Aguardando {pause_min_profiles}-{pause_max_profiles} segundos antes do proximo perfil...")
                pausa(min_tempo=pause_min_profiles, max_tempo=pause_max_profiles, jitter=2, nome="entre perfis")

            except KeyboardInterrupt:
                log.info("Interrupção detectada. Finalizando bot...")
                break
            except Exception as e:
                log.error(f"Erro ao processar perfil: {e}")
                # Pausa de erro antes de continuar
                pausa(min_tempo=30, max_tempo=60, jitter=5, nome="erro processamento")
                continue

        log.info(f"Processo finalizado! {perfis_processados} perfis processados, {reels_curtidos_total} reels curtidos.")
    except Exception as e:
        log.error(f"Ocorreu um erro durante a execução: {e}")
        sys.exit(1)
    finally:
        log.info("Fechando o navegador.")
        driver.quit()
        log.info("Bot finalizado.")
