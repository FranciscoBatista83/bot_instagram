import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import clicar_meu_perfil, clicar_seguidores, rolar_ate_ultimo_seguidor, extrair_urls_seguidores
from core.file_manager import gerenciar_arquivo_urls, limpar_duplicatas_arquivo
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    log.info("Iniciando o bot para acessar e coletar seguidores...")
    # Pausa inicial humanizada para simular abertura do navegador
    # pausa(min_tempo=8, max_tempo=15, jitter=0.5, nome="abertura navegador")
    usuario = os.getenv('INSTAGRAM_USER')
    senha = os.getenv('INSTAGRAM_PASSWORD')

    if not usuario or not senha:
        log.error("Credenciais não encontradas no arquivo .env. Verifique o arquivo e tente novamente.")
    else:
        driver = iniciar_driver()
        try:
            fazer_login(driver, usuario, senha)

            # Aguardar e tentar clicar no botão "Agora não" se o modal aparecer
            log.info("Verificando se há modal de salvar informações...")
            clicar_agora_nao(driver)

            # Aguardar um pouco e clicar no perfil
            log.info("Tentando acessar o perfil do usuário...")
            clicar_meu_perfil(driver)

            # Aguardar carregamento do perfil e clicar em seguidores
            log.info("Tentando acessar a lista de seguidores...")
            clicar_seguidores(driver)

            # Fazer scroll até carregar o último seguidor
            log.info("Fazendo scroll para carregar todos os seguidores...")
            rolar_ate_ultimo_seguidor(driver)

            # Extrair URLs dos seguidores e salvar no arquivo
            log.info("Extraindo URLs dos seguidores e atualizando arquivo...")
            urls_encontradas = extrair_urls_seguidores(driver)

            if urls_encontradas:
                sucesso = gerenciar_arquivo_urls(urls_encontradas, "seguidores.txt")
                if sucesso:
                    log.info("URLs dos seguidores salvas com sucesso!")

                    # Aguardar um pouco antes da limpeza
                    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após limpeza duplicatas")

                    # Limpar duplicatas do arquivo
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
        finally:
            log.info("Fechando o navegador.")
            driver.quit()
            log.info("Bot finalizado.")
