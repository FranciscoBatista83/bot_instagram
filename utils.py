import random
import time
from logger import log


def digitar_como_humano(elemento, texto):
    """
    Simula a digitação de um ser humano em um campo de texto.
    :param elemento: O elemento do campo de texto (input, textarea).
    :param texto: O texto a ser digitado.
    """
    for caractere in texto:
        elemento.send_keys(caractere)
        # Pausa mais longa e variável para evitar detecção (100ms a 400ms)
        time.sleep(random.uniform(0.1, 0.4))


def pausa(min_tempo=1.0, max_tempo=2.0, jitter=0.2, verbose=True, nome="personalizada"):
    """Pausa configurável com leve variação adicional (jitter) pra simular comportamento humano."""
    base = random.uniform(min_tempo, max_tempo)
    variacao = random.uniform(-jitter, jitter)
    duracao = round(base + variacao, 2)
    duracao = max(0, duracao)  # garante que não dá tempo negativo
    if verbose:
        log.info(f"Pausando por {duracao:.2f} segundos ({nome})...") # Removido emoji
    time.sleep(duracao)
