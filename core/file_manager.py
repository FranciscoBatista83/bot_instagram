import os
from logger import log

def gerenciar_arquivo_urls(urls_novas, nome_arquivo="seguidores.txt"):
    """Gerencia o arquivo de URLs: cria se não existir, lê existente e adiciona apenas URLs novas."""
    try:
        # Verificar se o arquivo existe
        if os.path.exists(nome_arquivo):
            log.info(f"Arquivo {nome_arquivo} encontrado. Lendo URLs existentes...")
            try:
                with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
                    urls_existentes = [linha.strip() for linha in arquivo if linha.strip()]
                log.info(f"Encontradas {len(urls_existentes)} URLs existentes.")
            except Exception as e:
                log.warning(f"Erro ao ler arquivo existente: {e}. Criando novo arquivo.")
                urls_existentes = []
        else:
            log.info(f"Arquivo {nome_arquivo} não encontrado. Será criado.")
            urls_existentes = []

        # Filtrar apenas URLs novas (não duplicar)
        urls_para_adicionar = []
        for url in urls_novas:
            if url not in urls_existentes:
                urls_para_adicionar.append(url)
                log.info(f"Nova URL para adicionar: {url}")
                from utils import pausa
                pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="entre processamentos urls")
            else:
                log.info(f"URL já existente (ignorada): {url}")

        # Adicionar URLs novas ao arquivo
        if urls_para_adicionar:
            try:
                with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
                    for url in urls_para_adicionar:
                        arquivo.write(url + "\n")
                        from utils import pausa
                        pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="entre processamentos urls")
                log.info(f"Adicionadas {len(urls_para_adicionar)} novas URLs ao arquivo {nome_arquivo}.")
            except Exception as e:
                log.error(f"Erro ao escrever no arquivo: {e}")
                return False
        else:
            log.info("Nenhuma URL nova para adicionar.")

        # Retornar estatísticas
        total_atual = len(urls_existentes) + len(urls_para_adicionar)
        log.info(f"Total de URLs no arquivo: {total_atual}")
        return True

    except Exception as e:
        log.error(f"Erro ao gerenciar arquivo de URLs: {e}")
        return False

def limpar_duplicatas_arquivo(nome_arquivo="seguidores.txt"):
    """Remove duplicatas do arquivo de URLs e reescreve ordenadamente."""
    try:
        log.info(f"Iniciando limpeza de duplicatas no arquivo {nome_arquivo}...")

        if not os.path.exists(nome_arquivo):
            log.warning(f"Arquivo {nome_arquivo} não encontrado para limpeza.")
            return False

        # Ler todas as URLs
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            todas_urls = [linha.strip() for linha in arquivo if linha.strip()]

        # Remover duplicatas mantendo ordem
        urls_unicas = []
        vistas = set()

        for url in todas_urls:
            if url not in vistas:
                urls_unicas.append(url)
                vistas.add(url)
                from utils import pausa
                pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="entre processamentos urls")

        # Reescribir arquivo com URLs únicas e ordenadas
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            for url in sorted(urls_unicas):  # Ordenar alfabeticamente
                arquivo.write(url + "\n")
                from utils import pausa
                pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="entre processamentos urls")

        duplicatas_removidas = len(todas_urls) - len(urls_unicas)
        log.info(f"Limpeza concluída! Removidas {duplicatas_removidas} duplicatas.")
        log.info(f"Total de URLs únicas no arquivo: {len(urls_unicas)}")

        return True

    except Exception as e:
        log.error(f"Erro ao limpar duplicatas do arquivo: {e}")
        return False

def ler_urls_arquivo(nome_arquivo="seguidores.txt"):
    """Lê todas as URLs do arquivo especificado."""
    try:
        if not os.path.exists(nome_arquivo):
            log.warning(f"Arquivo {nome_arquivo} não encontrado.")
            return []

        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            urls = [linha.strip() for linha in arquivo if linha.strip()]

        log.info(f"Lidas {len(urls)} URLs do arquivo {nome_arquivo}.")
        return urls

    except Exception as e:
        log.error(f"Erro ao ler arquivo de URLs: {e}")
        return []
