import logging
import sys

def setup_logger():
    """Configura o logger para exibir mensagens no console e salvar em um arquivo."""
    # Cria um logger
    logger = logging.getLogger('InstagramBot')
    logger.setLevel(logging.INFO)

    # Evita adicionar múltiplos handlers se a função for chamada mais de uma vez
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler para o arquivo de log
    file_handler = logging.FileHandler('bot.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para o console
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

# Cria uma instância única do logger para ser importada em outros módulos
log = setup_logger()
