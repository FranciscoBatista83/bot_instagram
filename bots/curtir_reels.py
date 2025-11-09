import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import interagir_com_reels
from logger import log
from utils import pausa
import os

if __name__ == "__main__":
    log.info("Iniciando o bot para curtir reels dos seguidores...")
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

            # Iniciar interação automática com reels de todos os perfis
            log.info("Iniciando interação automática com reels de todos os perfis...")
            sucesso = interagir_com_reels(driver, "seguidores.txt")
            if sucesso:
                log.info("Interação com reels concluída com sucesso!")
            else:
                log.warning("Erro na interação com reels.")

            log.info("Processo de curtir reels concluído!")
        except Exception as e:
            log.error(f"Ocorreu um erro durante a execução: {e}")
        finally:
            log.info("Fechando o navegador.")
            driver.quit()
            log.info("Bot finalizado.")
