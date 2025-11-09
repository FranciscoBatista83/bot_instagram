import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import visitar_perfil, clicar_seguidores, rolar_ate_ultimo_seguidor, extrair_urls_seguidores, seguir_perfis
from core.file_manager import ler_urls_arquivo
from logger import log
from utils import pausa
import os
import random

if __name__ == "__main__":
    log.info("Iniciando o bot para seguir perfis de seguidores de segundo nível...")
    
    usuario = os.getenv('INSTAGRAM_USER')
    senha = os.getenv('INSTAGRAM_PASSWORD')

    if not usuario or not senha:
        log.error("Credenciais não encontradas no arquivo .env. Verifique o arquivo e tente novamente.")
    else:
        driver = iniciar_driver()
        try:
            fazer_login(driver, usuario, senha)
            clicar_agora_nao(driver)

            urls_perfis_principais = ler_urls_arquivo("seguidores.txt")
            if not urls_perfis_principais:
                log.warning("Nenhuma URL de perfil principal encontrada em seguidores.txt para iniciar o processo.")
            else:
                log.info(f"Encontrados {len(urls_perfis_principais)} perfis principais para processar.")
                
                # Definir o número de ciclos (pode ser alterado)
                num_ciclos = 10 
                log.info(f"O bot irá rodar por {num_ciclos} ciclos.")

                for ciclo_atual in range(1, num_ciclos + 1):
                    log.info(f"=== INICIANDO CICLO {ciclo_atual}/{num_ciclos} ===")
                    
                    # Escolher um perfil principal aleatoriamente
                    url_principal = random.choice(urls_perfis_principais)
                    log.info(f"Perfil principal aleatório selecionado: {url_principal}")
                    
                    # Visitar o perfil principal
                    if not visitar_perfil(driver, url_principal):
                        log.warning(f"Não foi possível visitar o perfil principal: {url_principal}. Pulando para o próximo ciclo.")
                        continue
                    
                    # Clicar nos seguidores do perfil principal
                    if not clicar_seguidores(driver):
                        log.warning(f"Não foi possível acessar a lista de seguidores de {url_principal}. Pulando para o próximo ciclo.")
                        continue
                    
                    # Seguir 5 perfis de segundo nível diretamente
                    log.info(f"Iniciando processo de seguir 5 perfis de segundo nível de {url_principal}.")
                    seguir_perfis(driver, lote=5, pausa_entre_lotes_min=20, pausa_entre_lotes_max=30)
                    
                    log.info(f"Ciclo {ciclo_atual} concluído. Aguardando próxima iteração.")
                    # Pausa entre os ciclos
                    if ciclo_atual < num_ciclos:
                        log.info(f"Pausa entre ciclos...")
                        pausa(min_tempo=20 * 60, max_tempo=30 * 60, jitter=0.5, nome="entre ciclos de seguir")

            log.info("Processo de seguir perfis de segundo nível concluído.")
        except Exception as e:
            log.error(f"Ocorreu um erro durante a execução: {e}")
        finally:
            log.info("Fechando o navegador.")
            driver.quit()
            log.info("Bot finalizado.")
