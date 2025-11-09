from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import digitar_como_humano, pausa
from logger import log
from core.file_manager import ler_urls_arquivo

def clicar_meu_perfil(driver):
    """Clica no botão/link 'Perfil' para acessar o perfil do usuário usando múltiplas abordagens."""
    try:
        log.info("Procurando o botão/link do perfil...")
        # Aguardar um pouco para a página carregar completamente (pausa humanizada)
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="carregar perfil")

        # Método 1: Busca por imagem de perfil (mais confiável)
        try:
            log.info("🔍 Método 1: Buscando por imagem de perfil...")
            imagens_perfil = driver.find_elements(By.CSS_SELECTOR, "img[alt*='Foto do perfil de']")
            for img in imagens_perfil:
                try:
                    # Subir na árvore DOM para encontrar o link pai
                    link_pai = img
                    for _ in range(5):  # Subir até 5 níveis
                        link_pai = link_pai.find_element(By.XPATH, "..")
                        if link_pai.tag_name == "a" and link_pai.get_attribute("href"):
                            href = link_pai.get_attribute("href")
                            if href and href.startswith("https://www.instagram.com/") and not href.endswith("/explore/") and not href.endswith("/reels/"):
                                log.info(f"✅ Link do perfil encontrado por imagem: {href}")
                                # Usar JavaScript click para maior confiabilidade
                                driver.execute_script("arguments[0].click();", link_pai)
                                log.info("✅ Perfil acessado com sucesso via JavaScript!")
                                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após acessar perfil")
                                return True
                except:
                    continue
        except Exception as e:
            log.warning(f"⚠️ Erro no método 1: {e}")

        # Método 2: Busca por span com texto "Perfil"
        try:
            log.info("🔍 Método 2: Buscando por span com texto 'Perfil'...")
            spans_perfil = driver.find_elements(By.XPATH, "//span[text()='Perfil']")
            for span in spans_perfil:
                try:
                    # Subir na árvore DOM para encontrar o link pai
                    link_pai = span
                    for _ in range(5):  # Subir até 5 níveis
                        link_pai = link_pai.find_element(By.XPATH, "..")
                        if link_pai.tag_name == "a" and link_pai.get_attribute("href"):
                            href = link_pai.get_attribute("href")
                            if href and href.startswith("https://www.instagram.com/"):
                                log.info(f"✅ Link do perfil encontrado por span: {href}")
                                # Usar JavaScript click
                                driver.execute_script("arguments[0].click();", link_pai)
                                log.info("✅ Perfil acessado com sucesso via JavaScript!")
                                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="curta")
                                return True
                except:
                    continue
        except Exception as e:
            log.warning(f"⚠️ Erro no método 2: {e}")

        # Método 3: Busca por links de perfil genéricos
        try:
            log.info("🔍 Método 3: Buscando por links de perfil genéricos...")
            # Encontrar todos os links na barra lateral
            todos_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/']")
            for link in todos_links:
                try:
                    href = link.get_attribute("href")
                    if href and href.startswith("https://www.instagram.com/"):
                        path = href.replace("https://www.instagram.com/", "")
                        # Verificar se é um perfil de usuário (não uma página do sistema)
                        if (path and path != "/" and not path.startswith("explore/") and
                            not path.startswith("reels/") and not path.startswith("direct/") and
                            "/" not in path[1:] and len(path) > 1):  # Username válido
                            log.info(f"✅ Link de perfil genérico encontrado: {href}")
                            # Usar JavaScript click
                            driver.execute_script("arguments[0].click();", link)
                            log.info("✅ Perfil acessado com sucesso via JavaScript!")
                            pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="curta")
                            return True
                except:
                    continue
        except Exception as e:
            log.warning(f"⚠️ Erro no método 3: {e}")

        # Método 4: Busca por XPath (fallback)
        try:
            log.info("🔍 Método 4: Buscando por XPath (fallback)...")
            wait = WebDriverWait(driver, 5)
            link_perfil = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Perfil')]")))
            log.info("✅ Link do perfil encontrado por XPath")
            # Usar JavaScript click
            driver.execute_script("arguments[0].click();", link_perfil)
            log.info("✅ Perfil acessado com sucesso via JavaScript!")
            pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="curta")
            return True
        except Exception as e:
            log.warning(f"⚠️ Erro no método 4: {e}")

        log.warning("❌ Não foi possível encontrar o link/botão do perfil após tentar todas as abordagens.")
        return False

    except Exception as e:
        log.error(f"❌ Erro geral ao tentar acessar o perfil: {e}")
        return False

def clicar_seguidores(driver):
    """Clica no contador de seguidores para ver a lista de seguidores."""
    try:
        log.info("Procurando o contador de seguidores...")
        # Aguardar a página do perfil carregar completamente
        pausa(min_tempo=8, max_tempo=15, jitter=0.5, nome="carregar perfil seguidores")

        wait = WebDriverWait(driver, 15)

        # Método 1: Por texto exato usando XPath (procurando por "seguidores")
        try:
            contador_seguidores = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'seguidores')]")))
            log.info("Contador de seguidores encontrado por texto. Clicando...")
            pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="antes clicar seguidores")
            contador_seguidores.click()
            log.info("Seguidores acessado com sucesso!")
            pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="após clicar seguidores")
            return True
        except:
            pass

        # Método 2: Por classes CSS baseadas no HTML fornecido
        try:
            # Procurar por elementos com as classes características do contador
            elementos = driver.find_elements(By.CSS_SELECTOR, "[class*='x1lliihq'][class*='x1plvlek']")
            for elemento in elementos:
                if "seguidores" in elemento.text.lower():
                    log.info("Contador de seguidores encontrado por classe. Clicando...")
                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                    elemento.click()
                    log.info("Seguidores acessado com sucesso!")
                    pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="após clicar seguidores")
                    return True
        except:
            pass

        # Método 3: Por span com título numérico (número de seguidores)
        try:
            # Procurar spans que contenham números e "seguidores"
            spans = driver.find_elements(By.TAG_NAME, "span")
            for span in spans:
                texto = span.text.lower()
                if "seguidores" in texto and any(char.isdigit() for char in span.get_attribute("title") or ""):
                    log.info("Contador de seguidores encontrado por título numérico. Clicando...")
                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                    span.click()
                    log.info("Seguidores acessado com sucesso!")
                    pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="após clicar seguidores")
                    return True
        except:
            pass

        # Método 4: Busca mais ampla por elementos que contenham números e "seguidores"
        try:
            elementos_seguidores = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'SEGUIDORES', 'seguidores'), 'seguidores')]")
            for elemento in elementos_seguidores:
                if elemento.is_displayed() and any(char.isdigit() for char in elemento.text):
                    log.info("Elemento de seguidores encontrado por busca ampla. Clicando...")
                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                    elemento.click()
                    log.info("Seguidores acessado com sucesso!")
                    pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="após clicar seguidores método 4")
                    return True
        except:
            pass

        log.warning("Não foi possível encontrar o contador de seguidores.")
        return False

    except Exception as e:
        log.error(f"Erro ao tentar acessar seguidores: {e}")
        return False

def rolar_ate_ultimo_seguidor(driver):
    """Faz scroll dentro da caixa de seguidores até carregar o último elemento."""
    try:
        log.info("Iniciando scroll para carregar todos os seguidores...")

        # Aguardar um pouco para a lista carregar inicialmente
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="iniciar scroll seguidores")

        # Tentar encontrar a área de scroll (caixa de seguidores)
        scroll_container = None

        # Método 1: Procurar por divs com scroll (altura específica e overflow)
        try:
            # Baseado na estrutura do HTML, procurar pela área de scroll principal
            containers = driver.find_elements(By.CSS_SELECTOR, "[class*='x6nl9eh'][class*='x1a5l9x9']")
            for container in containers:
                if container.is_displayed() and container.size['height'] > 200:
                    scroll_container = container
                    log.info("Área de scroll encontrada por classe CSS.")
                    break
        except:
            pass

        # Método 2: Procurar pela div com altura específica e scroll
        if not scroll_container:
            try:
                containers = driver.find_elements(By.TAG_NAME, "div")
                for container in containers:
                    if (container.is_displayed() and
                        container.size['height'] > 300 and
                        "overflow" in container.get_attribute("style").lower()):
                        scroll_container = container
                        log.info("Área de scroll encontrada por propriedades de estilo.")
                        break
            except:
                pass

        # Método 3: Usar o body como fallback se não encontrar container específico
        if not scroll_container:
            scroll_container = driver.find_element(By.TAG_NAME, "body")
            log.info("Usando body como área de scroll (fallback).")

        # Fazer scroll até o final com múltiplas tentativas
        max_scroll_attempts = 10
        previous_height = 0

        for attempt in range(max_scroll_attempts):
            # Fazer scroll até o final
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_container)

            # Aguardar carregamento
            pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="aguardar carregamento scroll")

            # Verificar se carregou mais conteúdo
            try:
                current_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_container)

                if current_height == previous_height:
                    log.info(f"Scroll concluído no attempt {attempt + 1}. Não há mais conteúdo para carregar.")
                    break
                else:
                    previous_height = current_height
                    log.info(f"Carregado mais conteúdo. Altura atual: {current_height}px")

            except:
                log.info(f"Erro ao verificar altura do scroll no attempt {attempt + 1}")
                break

        # Aguardar final para garantir que tudo carregou
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="finalizar scroll seguidores")

        # Verificar se o último elemento apareceu (elemento de loading desapareceu)
        try:
            loading_elements = driver.find_elements(By.CSS_SELECTOR, "[data-visualcompletion='loading-state']")
            if loading_elements:
                log.info("Aguardando fim do carregamento...")
                wait = WebDriverWait(driver, 10)
                wait.until(EC.invisibility_of_element(loading_elements[0]))
                log.info("Carregamento concluído!")
        except:
            pass

        log.info("Scroll nos seguidores concluído com sucesso!")
        return True

    except Exception as e:
        log.error(f"Erro durante o scroll dos seguidores: {e}")
        return False

def extrair_urls_seguidores(driver):
    """Extrai todas as URLs dos perfis dos seguidores visíveis na página."""
    try:
        log.info("Extraindo URLs dos seguidores...")

        # Aguardar um pouco para garantir que tudo carregou
        pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="extrair urls seguidores")

        urls_encontradas = []

        # Lista negra de termos que indicam elementos da interface (não perfis de usuários)
        blacklist_terms = [
            'accounts', 'archive', 'explore', 'web', 'reels', 'direct',
            'legal', 'privacy', 'terms', 'help', 'about', 'blog',
            'jobs', 'api', 'developer', 'press', 'advertising'
        ]

        # Método 1: Procurar por links de perfil dentro da estrutura de seguidores
        try:
            log.info("Método 1: Extraindo links de perfil...")
            # Baseado na estrutura HTML fornecida, procurar por links de perfil
            links_perfil = driver.find_elements(By.CSS_SELECTOR, "a[href*='/'][class*='x1i10hfl']")

            for link in links_perfil:
                href = link.get_attribute("href")
                if href and "/p/" not in href and len(href) > 10:  # Filtrar apenas perfis, não posts
                    # Extrair username da URL
                    if href.startswith("https://www.instagram.com/"):
                        username = href.replace("https://www.instagram.com/", "").split("/")[0]

                        # Filtrar elementos da interface usando lista negra
                        if (username and
                            username not in [url.split("/")[-2] for url in urls_encontradas] and
                            not any(term in username.lower() for term in blacklist_terms) and
                            username.replace("_", "").replace(".", "").isalnum() and  # Username válido
                            len(username) >= 3 and len(username) <= 30):  # Comprimento típico de username

                            urls_encontradas.append(f"https://www.instagram.com/{username}/")
                            log.info(f"Perfil válido encontrado: https://www.instagram.com/{username}/")
                            pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="entre extrações de perfil")
        except Exception as e:
            log.warning(f"Erro no método 1 de extração: {e}")

        log.info(f"Total de perfis válidos encontrados: {len(urls_encontradas)}")
        return urls_encontradas

    except Exception as e:
        log.error(f"Erro ao extrair URLs dos seguidores: {e}")
        return []

def visitar_perfil(driver, url_perfil=None, nome_arquivo="seguidores.txt"):
    """Visita um perfil específico ou escolhe aleatoriamente do arquivo."""
    try:
        # Se não foi fornecida uma URL específica, escolher aleatoriamente do arquivo
        if not url_perfil:
            urls_disponiveis = ler_urls_arquivo(nome_arquivo)
            if not urls_disponiveis:
                log.warning("Nenhuma URL disponível para visitar.")
                return False

            import random
            url_perfil = random.choice(urls_disponiveis)
            log.info(f"Perfil escolhido aleatoriamente: {url_perfil}")

        # Navegar para o perfil
        log.info(f"Navegando para o perfil: {url_perfil}")
        driver.get(url_perfil)

        # Aguardar carregamento do perfil com pausa humanizada
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="carregar perfil aleatório")

        # Verificar se o perfil carregou corretamente
        try:
            # Aguardar um elemento típico de perfil (como nome de usuário ou bio)
            wait = WebDriverWait(driver, 10)
            # Tentar encontrar elementos que indiquem que o perfil carregou
            elementos_perfil = wait.until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, "[class*='x1lliihq']") or
                              driver.find_elements(By.TAG_NAME, "h1") or
                              driver.find_elements(By.CSS_SELECTOR, "[class*='x9f619']")
            )

            if elementos_perfil:
                log.info("Perfil carregado com sucesso!")
                # Pausa adicional para simular visualização humanizada
                pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="visualizar perfil aleatório")
                return True
            else:
                log.warning("Perfil pode não ter carregado corretamente.")
                return False

        except Exception as e:
            log.warning(f"Erro ao verificar carregamento do perfil: {e}")
            return False

    except Exception as e:
        log.error(f"Erro ao visitar perfil: {e}")
        return False

def visitar_perfil_especifico(driver, url_perfil):
    """Visita um perfil específico passando a URL diretamente."""
    return visitar_perfil(driver, url_perfil)

def interagir_com_reels(driver, nome_arquivo="seguidores.txt"):
    """Interage com reels de todos os perfis do arquivo em ordem: curte o primeiro reel se não estiver curtido."""
    try:
        log.info("Iniciando interação automática com reels de todos os perfis...")

        # Ler todos os perfis do arquivo
        urls_perfis = ler_urls_arquivo(nome_arquivo)
        if not urls_perfis:
            log.warning("Nenhum perfil encontrado no arquivo.")
            return False

        log.info(f"Encontrados {len(urls_perfis)} perfis para processar em ordem.")
        perfis_processados = 0
        reels_curtidos = 0

        # Para cada perfil EM ORDEM (não aleatório)
        for i, url_perfil in enumerate(urls_perfis):
            try:
                log.info(f"Processando perfil {i+1}/{len(urls_perfis)}: {url_perfil}")

                # Navegar para o perfil
                driver.get(url_perfil)
                pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="aguarda carregar perfil")

                # Tentar encontrar reels no perfil
                reels_encontrados = encontrar_reels_perfil(driver)

                if reels_encontrados:
                    # Pegar o primeiro reel
                    primeiro_reel = reels_encontrados[0]
                    log.info("Encontrado primeiro reel, navegando...")

                    # Clicar no primeiro reel
                    primeiro_reel.click()
                    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="aguardar reel abrir")

                    # Verificar se consegue curtir
                    if curtir_reel(driver):
                        reels_curtidos += 1
                        log.info(f"✓ Reel curtido com sucesso em {url_perfil}")
                    else:
                        log.info(f"○ Reel já estava curtido ou não foi possível curtir em {url_perfil}")
                else:
                    log.info(f"○ Nenhum reel encontrado em {url_perfil}")

                perfis_processados += 1

                # Pausa entre perfis para não ser muito rápido
                if i < len(urls_perfis) - 1:  # Não pausar no último
                    pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="entre perfis")

            except Exception as e:
                log.error(f"Erro ao processar perfil {url_perfil}: {e}")
                continue

        log.info(f"Interação automática concluída! {perfis_processados} perfis processados, {reels_curtidos} reels curtidos.")
        return True

    except Exception as e:
        log.error(f"Erro geral na interação com reels: {e}")
        return False

def encontrar_reels_perfil(driver):
    """Encontra todos os reels visíveis em um perfil."""
    try:
        # Aguardar um pouco para o perfil carregar completamente
        pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="aguarda reels carregar")

        # Procurar por elementos de reels (ícones de clipe)
        reels = []

        # Método 1: Procurar por elementos com ícone de clipe (reels)
        try:
            # Baseado no HTML fornecido, procurar por elementos com SVG de clipe
            elementos_reels = driver.find_elements(By.CSS_SELECTOR, "[class*='x1lliihq'][class*='x1n2onr6'] svg[aria-label='Clipe']")

            # Subir na árvore DOM para encontrar o link do reel
            for svg_clipe in elementos_reels:
                try:
                    # Subir 4 níveis na árvore DOM para encontrar o link <a>
                    link_reel = svg_clipe
                    for _ in range(4):  # Subir 4 níveis
                        link_reel = link_reel.find_element(By.XPATH, "..")

                    if link_reel.tag_name == 'a' and link_reel.get_attribute('href'):
                        reels.append(link_reel)
                except:
                    continue

        except Exception as e:
            log.warning(f"Erro ao procurar reels método 1: {e}")

        # Método 2: Procurar por links que contenham "/reel/" na URL
        try:
            links_reels = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/reel/']")
            for link in links_reels:
                if link not in reels:  # Evitar duplicatas
                    reels.append(link)
        except Exception as e:
            log.warning(f"Erro ao procurar reels método 2: {e}")

        log.info(f"Encontrados {len(reels)} reels no perfil.")
        return reels[:3]  # Retornar no máximo 3 reels

    except Exception as e:
        log.error(f"Erro ao encontrar reels: {e}")
        return []

def verificar_estado_curtida(botao_curtir):
    """Verifica se um reel já está curtido analisando o elemento do botão."""
    try:
        # Método 1: Verificar atributo fill do SVG
        fill_attr = botao_curtir.get_attribute("fill")
        if fill_attr and fill_attr not in ["none", "currentColor"]:
            return True  # Está preenchido = curtido

        # Método 2: Verificar classes do elemento pai
        try:
            parent_element = botao_curtir.find_element(By.XPATH, "..")
            classes_parent = parent_element.get_attribute("class")
            if classes_parent and ("liked" in classes_parent.lower() or "fill" in classes_parent.lower()):
                return True  # Pai indica que está curtido
        except:
            pass

        # Método 3: Verificar se há elementos de animação de curtir
        try:
            # Quando curte, geralmente aparece uma animação ou elementos específicos
            animacoes = botao_curtir.find_elements(By.XPATH, "../../..//*[contains(@class, 'like')]")
            if animacoes:
                return True
        except:
            pass

        return False  # Não está curtido

    except Exception as e:
        log.warning(f"Erro ao verificar estado de curtida: {e}")
        return False

def curtir_reel(driver):
    """Tenta curtir um reel se não estiver curtido usando JavaScript click."""
    try:
        log.info("💖 Tentando curtir reel...")
        # Aguardar um pouco para o reel carregar completamente
        pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="curta")

        # Método 2: Procurar especificamente pela estrutura do HTML fornecida (PRIORIDADE 1)
        try:
            log.info("🔍 Método 2: Procurando pela estrutura exata do HTML...")

            # Baseado no HTML fornecido, procurar pela section específica
            sections = driver.find_elements(By.CSS_SELECTOR, "section[class*='x78zum5'][class*='x1q0g3np']")

            for section in sections:
                try:
                    # Dentro da section, procurar o botão de curtir
                    botoes_curtir = section.find_elements(By.CSS_SELECTOR, "svg[aria-label='Curtir']")
                    log.info(f"  🎯 Encontrados {len(botoes_curtir)} SVGs de curtir na section")

                    for svg in botoes_curtir:
                        try:
                            # Subir na árvore DOM para encontrar o botão clicável
                            botao = svg
                            for _ in range(3):  # Subir 3 níveis baseado na estrutura
                                botao = botao.find_element(By.XPATH, "..")

                            if botao and botao.get_attribute("role") == "button":
                                log.info("    ✅ Botão de curtir encontrado na estrutura correta")

                                if botao.is_displayed() and botao.is_enabled():
                                    # Verificar estado
                                    fill_attr = svg.get_attribute("fill")
                                    log.info(f"    🎨 Atributo fill: {fill_attr}")

                                    if fill_attr and fill_attr not in ["currentColor"]:
                                        log.info("    ❤️ Reel já está curtido")
                                        return False
                                    else:
                                        log.info("    🤍 Curtindo reel...")
                                        try:
                                            driver.execute_script("arguments[0].click();", botao)
                                            log.info("    ✅ Clique JavaScript realizado! [MÉTODO 2 - Estrutura HTML]")
                                            pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                            return True
                                        except:
                                            driver.execute_script("arguments[0].scrollIntoView();", botao)
                                            time.sleep(0.5)
                                            driver.execute_script("arguments[0].click();", botao)
                                            log.info("    ✅ Clique JavaScript após scroll! [MÉTODO 2 - Fallback]")
                                            pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                            return True
                        except:
                            continue

                except Exception as e:
                    log.warning(f"  ⚠️ Erro ao processar section: {e}")
                    continue

        except Exception as e:
            log.warning(f"⚠️ Erro no método 2: {e}")

        # Método 2.1: Procurar pela estrutura mais específica baseada no HTML fornecido
        try:
            log.info("🔍 Método 2.1: Procurando pela estrutura completa do HTML fornecido...")

            # Estrutura mais específica baseada no HTML completo
            botoes_curtir = driver.find_elements(By.CSS_SELECTOR, "section[class*='x78zum5'][class*='x1q0g3np'] span[class*='x1rg5ohu'] div[class*='x1ypdohk'] div[role='button']")

            log.info(f"  🎯 Encontrados {len(botoes_curtir)} botões de curtir na estrutura completa")

            for botao in botoes_curtir:
                try:
                    if botao.is_displayed() and botao.is_enabled():
                        log.info("    ✅ Botão de curtir encontrado na estrutura completa")

                        # Verificar se contém SVG de curtir
                        svg_curtir = botao.find_elements(By.CSS_SELECTOR, "svg[aria-label='Curtir']")
                        if svg_curtir:
                            svg = svg_curtir[0]
                            fill_attr = svg.get_attribute("fill")
                            log.info(f"    🎨 Atributo fill: {fill_attr}")

                            if fill_attr and fill_attr not in ["currentColor"]:
                                log.info("    ❤️ Reel já está curtido")
                                return False
                            else:
                                log.info("    🤍 Curtindo reel...")
                                try:
                                    driver.execute_script("arguments[0].click();", botao)
                                    log.info("    ✅ Clique JavaScript realizado! [MÉTODO 2.1 - Estrutura Completa]")
                                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                    return True
                                except:
                                    driver.execute_script("arguments[0].scrollIntoView();", botao)
                                    time.sleep(0.5)
                                    driver.execute_script("arguments[0].click();", botao)
                                    log.info("    ✅ Clique JavaScript após scroll! [MÉTODO 2.1 - Fallback]")
                                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                    return True
                except Exception as e:
                    log.warning(f"    ⚠️ Erro ao processar botão: {e}")
                    continue

        except Exception as e:
            log.warning(f"⚠️ Erro no método 2.1: {e}")

        # Método 1: Procurar especificamente por botão de curtir do reel (PRIORIDADE 2)
        try:
            log.info("🔍 Método 1: Procurando botão de curtir...")
            botoes_curtir = driver.find_elements(By.CSS_SELECTOR, "svg[aria-label='Curtir']")
            log.info(f"  🎯 Encontrados {len(botoes_curtir)} botões com aria-label='Curtir'")

            for i, botao in enumerate(botoes_curtir):
                try:
                    log.info(f"  🎯 Verificando botão {i+1}...")

                    if botao.is_displayed() and botao.is_enabled():
                        log.info("    ✅ Botão visível e habilitado")
                        # Verificar se já está curtido
                        if verificar_estado_curtida(botao):
                            log.info("    ❤️ Reel já está curtido")
                            return False
                        else:
                            log.info("    🤍 Curtindo reel...")
                            # Usar JavaScript click como método principal
                            try:
                                driver.execute_script("arguments[0].click();", botao)
                                log.info("    ✅ Clique JavaScript realizado! [MÉTODO 1 - Botão SVG direto]")
                                pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                return True
                            except Exception as e:
                                log.warning(f"    ❌ Erro no clique JavaScript: {e}")
                                # Tentar scroll como último recurso
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView();", botao)
                                    time.sleep(0.5)
                                    driver.execute_script("arguments[0].click();", botao)
                                    log.info("    ✅ Clique JavaScript após scroll! [MÉTODO 1 - Fallback com scroll]")
                                    pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                                    return True
                                except Exception as e2:
                                    log.warning(f"    ❌ Erro mesmo após scroll: {e2}")
                                    continue
                    else:
                        log.info("    ❌ Botão não visível ou desabilitado")
                except Exception as e:
                    log.warning(f"  ⚠️ Erro ao processar botão {i+1}: {e}")
                    continue

        except Exception as e:
            log.warning(f"⚠️ Erro no método 1: {e}")

        # Método 3: Tentar clicar diretamente no SVG (PRIORIDADE 3)
        try:
            log.info("🔍 Método 3: Tentando clicar diretamente no SVG...")
            svg_curtir = driver.find_elements(By.CSS_SELECTOR, "svg[aria-label='Curtir']")

            for svg in svg_curtir[:1]:
                if svg.is_displayed():
                    log.info("  🎯 SVG de curtir encontrado, tentando clique direto...")
                    try:
                        driver.execute_script("arguments[0].click();", svg)
                        log.info("  ✅ Clique JavaScript no SVG! [MÉTODO 3 - SVG direto]")
                        pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                        return True
                    except Exception as e:
                        log.warning(f"  ❌ Erro no clique JavaScript: {e}")
                        try:
                            driver.execute_script("arguments[0].scrollIntoView();", svg)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", svg)
                            log.info("  ✅ Clique JavaScript no SVG após scroll! [MÉTODO 3 - Fallback com scroll]")
                            pausa(min_tempo=0.2, max_tempo=0.8, jitter=0.1, nome="muito curta")
                            return True
                        except Exception as e2:
                            log.warning(f"  ❌ Erro mesmo após scroll: {e2}")
                            continue

        except Exception as e:
            log.warning(f"⚠️ Erro no método 3: {e}")

        log.info("❌ Nenhum botão de curtir encontrado ou reel já curtido.")
        return False

    except Exception as e:
        log.error(f"Erro ao tentar curtir reel: {e}")
        return False

def clicar_seguindo(driver):
    """Clica no contador de 'seguindo' para ver a lista de perfis que o usuário segue."""
    try:
        log.info("Procurando o contador de 'seguindo'...")
        pausa(min_tempo=8, max_tempo=15, jitter=0.5, nome="carregar perfil seguindo")

        wait = WebDriverWait(driver, 15)
        
        # Tenta encontrar o link que contém 'seguindo' no texto.
        contador_seguindo = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'seguindo')]")))
        log.info("Contador de 'seguindo' encontrado. Clicando...")
        contador_seguindo.click()
        
        log.info("Lista de 'seguindo' acessada com sucesso!")
        pausa(min_tempo=4, max_tempo=8, jitter=0.3, nome="após clicar seguindo")
        return True
    except Exception as e:
        log.error(f"Erro ao clicar em 'seguindo': {e}")
        return False

def deixar_de_seguir_perfis(driver, lote=10):
    """Deixa de seguir perfis em lotes controlados com pausas entre execuções.

    Args:
        driver: Instância do webdriver
        lote: Quantidade de perfis para deixar de seguir por execução (padrão: 10)
    """
    try:
        log.info(f"Iniciando processo de unfollow em lotes de {lote} perfis com pausa de 15-30 minutos entre lotes.")
        lote_atual = 0
        total_perfis_deixados_de_seguir = 0

        while True:  # Loop infinito até não haver mais perfis para deixar de seguir
            lote_atual += 1
            perfis_deixados_de_seguir_lote = 0

            log.info(f"=== LOTE {lote_atual} - Buscando perfis para deixar de seguir ===")

            # Tentar fazer scroll para carregar mais perfis se necessário
            try:
                # Scroll down para carregar mais perfis
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                pausa(min_tempo=2, max_tempo=4, jitter=0.2, nome="scroll carregar mais perfis")
            except:
                pass

            # Encontra todos os botões "Seguindo" visíveis
            botoes_seguindo = driver.find_elements(By.XPATH, "//button[div/div[contains(text(), 'Seguindo')]]")

            if not botoes_seguindo:
                log.info("Nenhum botão 'Seguindo' encontrado. Processo concluído!")
                break

            log.info(f"Encontrados {len(botoes_seguindo)} perfis disponíveis no lote {lote_atual}.")

            # Processa apenas o lote atual
            for i, botao in enumerate(botoes_seguindo):
                if perfis_deixados_de_seguir_lote >= lote:
                    log.info(f"Lote {lote_atual} concluído: {perfis_deixados_de_seguir_lote} perfis deixados de seguir.")
                    break

                try:
                    log.info(f"Processando perfil {i+1}/{min(lote, len(botoes_seguindo))} do lote {lote_atual}")

                    # Clica no botão "Seguindo"
                    driver.execute_script("arguments[0].click();", botao)
                    log.info("Botão 'Seguindo' clicado.")
                    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após clicar seguindo")

                    # Confirma a ação de "Deixar de seguir"
                    botao_confirmar = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Deixar de seguir')]"))
                    )
                    driver.execute_script("arguments[0].click();", botao_confirmar)
                    log.info("Ação de 'Deixar de seguir' confirmada.")

                    perfis_deixados_de_seguir_lote += 1
                    total_perfis_deixados_de_seguir += 1
                    log.info(f"Perfil {total_perfis_deixados_de_seguir} deixado de seguir com sucesso!")

                    # Pausa entre unfollows para simular comportamento humano
                    pausa(min_tempo=8, max_tempo=15, jitter=0.5, nome="entre unfollows")

                except Exception as e:
                    log.error(f"Erro ao tentar deixar de seguir um perfil: {e}")
                    continue

            # Verifica se conseguiu processar algum perfil neste lote
            if perfis_deixados_de_seguir_lote == 0:
                log.info("Nenhum perfil foi processado neste lote. Processo concluído!")
                break

            # Se ainda há perfis para processar, aguarda antes do próximo lote
            if perfis_deixados_de_seguir_lote >= lote:
                log.info("⏰ Aguardando 15-30 minutos antes do próximo lote...")
                pausa(min_tempo=900, max_tempo=1800, jitter=30, nome="pausa entre lotes")
                log.info(f"⏰ Pausa concluída. Iniciando lote {lote_atual + 1}...")

        log.info(f"🎉 Processo de unfollow completamente concluído! Total de perfis deixados de seguir: {total_perfis_deixados_de_seguir}")
        return True

    except Exception as e:
        log.error(f"Erro geral ao deixar de seguir perfis: {e}")
        return False

def seguir_perfis(driver, lote=5, pausa_entre_lotes_min=15, pausa_entre_lotes_max=30):
    """
    Segue perfis em lotes controlados com pausas entre execuções.
    Procura por botões 'Seguir' e clica neles.

    Args:
        driver: Instância do webdriver.
        lote: Quantidade de perfis para seguir por execução (padrão: 5).
        pausa_entre_lotes_min: Tempo mínimo de pausa entre lotes em minutos.
        pausa_entre_lotes_max: Tempo máximo de pausa entre lotes em minutos.
    """
    try:
        log.info(f"Iniciando processo de seguir perfis em lotes de {lote} perfis com pausa de {pausa_entre_lotes_min}-{pausa_entre_lotes_max} minutos entre lotes.")
        lote_atual = 0
        total_perfis_seguidos = 0

        while True:  # Loop infinito até não haver mais perfis para seguir
            lote_atual += 1
            perfis_seguidos_lote = 0

            log.info(f"=== LOTE {lote_atual} - Buscando perfis para seguir ===")

            # Tentar fazer scroll para carregar mais perfis se necessário
            try:
                # Scroll down para carregar mais perfis
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                pausa(min_tempo=2, max_tempo=4, jitter=0.2, nome="scroll carregar mais perfis")
            except:
                pass

            # Encontra todos os botões "Seguir" visíveis
            # Procurar por botões que contenham "Seguir" no texto ou aria-label
            botoes_seguir = driver.find_elements(By.XPATH, "//button[contains(., 'Seguir') or @aria-label='Seguir']")

            # Filtrar apenas os botões que realmente são de seguir e não de "Seguindo" ou outros
            botoes_seguir_validos = []
            for botao in botoes_seguir:
                if botao.is_displayed() and botao.is_enabled() and "Seguindo" not in botao.text:
                    botoes_seguir_validos.append(botao)

            if not botoes_seguir_validos:
                log.info("Nenhum botão 'Seguir' encontrado. Processo de seguir concluído!")
                break

            log.info(f"Encontrados {len(botoes_seguir_validos)} perfis disponíveis para seguir no lote {lote_atual}.")

            # Processa apenas o lote atual
            for i, botao in enumerate(botoes_seguir_validos):
                if perfis_seguidos_lote >= lote:
                    log.info(f"Lote {lote_atual} concluído: {perfis_seguidos_lote} perfis seguidos.")
                    break

                try:
                    log.info(f"Processando perfil {i+1}/{min(lote, len(botoes_seguir_validos))} do lote {lote_atual}")

                    # Clica no botão "Seguir"
                    driver.execute_script("arguments[0].click();", botao)
                    log.info("Botão 'Seguir' clicado.")
                    pausa(min_tempo=1.5, max_tempo=3.0, jitter=0.3, nome="após clicar seguir")

                    perfis_seguidos_lote += 1
                    total_perfis_seguidos += 1
                    log.info(f"Perfil {total_perfis_seguidos} seguido com sucesso!")

                    # Pausa entre follows para simular comportamento humano
                    pausa(min_tempo=8, max_tempo=15, jitter=0.5, nome="entre follows")

                except Exception as e:
                    log.error(f"Erro ao tentar seguir um perfil: {e}")
                    continue

            # Verifica se conseguiu processar algum perfil neste lote
            if perfis_seguidos_lote == 0:
                log.info("Nenhum perfil foi processado neste lote. Processo de seguir concluído!")
                break

            # Se ainda há perfis para processar, aguarda antes do próximo lote
            if perfis_seguidos_lote >= lote:
                log.info(f"⏰ Aguardando {pausa_entre_lotes_min}-{pausa_entre_lotes_max} minutos antes do próximo lote...")
                pausa(min_tempo=pausa_entre_lotes_min * 60, max_tempo=pausa_entre_lotes_max * 60, jitter=30, nome="pausa entre lotes de seguir")
                log.info(f"⏰ Pausa concluída. Iniciando lote {lote_atual + 1}...")

        log.info(f"🎉 Processo de seguir perfis completamente concluído! Total de perfis seguidos: {total_perfis_seguidos}")
        return True

    except Exception as e:
        log.error(f"Erro geral ao seguir perfis: {e}")
        return False
