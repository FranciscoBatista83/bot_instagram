import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import clicar_meu_perfil, clicar_seguindo, deixar_de_seguir_perfis
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    log.info("Iniciando o bot para deixar de seguir perfis...")
    # pausa(min_tempo=2, max_tempo=7, jitter=0.2, nome="abertura navegador")
    usuario = os.getenv('INSTAGRAM_USER')
    senha = os.getenv('INSTAGRAM_PASSWORD')
    
    if not usuario or not senha:
        log.error("Credenciais não encontradas no arquivo .env.")
    else:
        driver = iniciar_driver()
        try:
            fazer_login(driver, usuario, senha)
            clicar_agora_nao(driver)
            clicar_meu_perfil(driver)
            clicar_seguindo(driver)
            deixar_de_seguir_perfis(driver, lote=10)

            log.info("Processo de deixar de seguir concluído.")
        except Exception as e:
            log.error(f"Ocorreu um erro durante a execução: {e}")
        finally:
            log.info("Fechando o navegador.")
            driver.quit()
            log.info("Bot finalizado.")
