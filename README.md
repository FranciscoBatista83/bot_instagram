# Bot Instagram - Automacao Completa

Bot automatizado para Instagram com multiplas funcionalidades: extracao de seguidores, interacao com reels, visita de perfis e sistema de unfollow inteligente.

## Funcionalidades

### Implementadas

1. **Extracao Inteligente de Seguidores**
   - Filtra apenas perfis de usuarios reais
   - Lista negra de termos para URLs invalidas
   - Validacao rigorosa de usernames (3-30 caracteres)

2. **Visitacao de Perfis**
   - Visita perfis aleatoriamente do arquivo `seguidores.txt`
   - Visita perfis especificos por URL
   - Verificacao de carregamento do perfil

3. **Interacao com Reels**
   - Encontra e acessa o primeiro reel de cada perfil
   - Verifica estado de curtida (coracao preenchido vs vazio)
   - Curte automaticamente apenas se necessario
   - Processa todos os perfis em ordem sequencial

4. **Sistema de Unfollow Inteligente**
   - Deixa de seguir perfis em lotes controlados
   - Pausas de 15-30 minutos entre lotes
   - Evita deteccao por comportamento robotico
   - Loop automatico ate completar todos os perfis

5. **Sistema de Pausas Humanizadas**
   - Todas as pausas usam funcoes centralizadas do `utils.py`
   - Variacoes aleatorias para simular comportamento humano
   - Multiplos tipos de pausa (curta, media, longa)

## Estrutura do Projeto

```
bot_instagram/
├── bots/
│   ├── __init__.py
│   ├── acessar_seguidores.py      # Extracao de seguidores
│   ├── curtir_reels.py           # Interacao com reels
│   └── deixar_de_seguir.py       # Sistema de unfollow
├── core/
│   ├── __init__.py
│   ├── actions.py                # Funcoes principais de automacao
│   ├── browser.py                # Gerenciamento do navegador
│   └── file_manager.py           # Gerenciamento de arquivos
├── logger.py                     # Sistema de logging
├── utils.py                      # Funcoes utilitarias e pausas
├── requirements.txt              # Dependencias Python
├── .env                          # Credenciais (nao versionado)
├── seguidores.txt                # Lista de perfis extraidos
└── README.md                     # Esta documentacao
```

## Como Usar

### 1. Instalacao

```bash
# Clone o repositorio
git clone <url-do-repositorio>
cd bot_instagram

# Instale as dependencias
pip install -r requirements.txt
```

### 2. Configuracao

Configure suas credenciais no arquivo `.env`:
```env
INSTAGRAM_USER=seu_usuario_aqui
INSTAGRAM_PASSWORD=sua_senha_aqui
```

### 3. Execucao dos Bots

#### Extrair Seguidores:
```bash
python bots/acessar_seguidores.py
```

#### Curtir Reels:
```bash
python bots/curtir_reels.py
```

#### Deixar de Seguir Perfis:
```bash
python bots/deixar_de_seguir.py
```

## Detalhes das Funcionalidades

### Sistema de Unfollow Inteligente
- **Lotes configuraveis**: Padrao 10 perfis por lote
- **Pausas inteligentes**: 15-30 minutos entre lotes
- **Loop automatico**: Continua ate completar todos os perfis
- **Scroll automatico**: Carrega mais perfis conforme necessario

**Exemplo de execucao:**
```
=== LOTE 1 - Buscando perfis para deixar de seguir ===
Encontrados 25 perfis disponiveis no lote 1.
Lote 1 concluido: 10 perfis deixados de seguir.
Aguardando 15-30 minutos antes do proximo lote...
=== LOTE 2 - Buscando perfis para deixar de seguir ===
Encontrados 15 perfis disponiveis no lote 2.
Lote 2 concluido: 10 perfis deixados de seguir.
Processo de unfollow completamente concluido! Total: 20 perfis.
```

### Interacao com Reels
- **Processamento sequencial**: Todos os perfis em ordem
- **Detecção inteligente**: Multiplos metodos para encontrar reels
- **Verificacao de estado**: So curte se necessario
- **Relatorio visual**: (curtido) / (ja curtido)

### Extracao de Seguidores
- **Filtragem avancada**: Remove elementos da interface
- **Lista negra**: 15+ termos filtrados
- **Validacao**: Usernames validos apenas

## Melhorias Tecnicas

### Sistema de Pausas Centralizado
```python
# Exemplo de uso das pausas
pausa(min_tempo=2.0, max_tempo=5.0, jitter=0.3, nome="carregar pagina")
```

### Lista Negra de Filtragem
```python
blacklist_terms = [
    'accounts', 'archive', 'explore', 'web', 'reels', 'direct',
    'legal', 'privacy', 'terms', 'help', 'about', 'blog',
    'jobs', 'api', 'developer', 'press', 'advertising'
]
```

### Verificacao Inteligente de Curtidas
- Analise do atributo `fill` do SVG
- Verificacao de classes do elemento pai
- Multiplos metodos de fallback

## Logs e Monitoramento

O sistema gera logs detalhados em `bot.log` incluindo:
- Status de cada operacao
- Perfis processados
- Warnings e erros
- Estatisticas finais

## Segurança e Etica

- **Modo incognito** ativado
- **Pausas humanizadas** para evitar deteccao
- **Limitacao de acoes** por lote
- **Tratamento robusto** de erros
- **Uso responsavel** - respeite os termos do Instagram

## Dependencias

```txt
selenium>=4.15.0          # Automacao web
python-dotenv>=1.0.0      # Gerenciamento de variaveis de ambiente
webdriver-manager>=4.0.0  # Gerenciamento automatico de drivers
requests>=2.31.0          # Requisicoes HTTP
urllib3>=2.0.0           # Cliente HTTP
certifi>=2023.7.22       # Certificados SSL
charset-normalizer>=3.2.0 # Codificacao de caracteres
idna>=3.4                # Internacionalizacao de dominios
```

## Exemplo de Uso Programatico

```python
from core.browser import iniciar_driver, fazer_login, clicar_agora_nao
from core.actions import clicar_meu_perfil, clicar_seguindo, deixar_de_seguir_perfis

# Exemplo: Sistema completo de unfollow
driver = iniciar_driver()
fazer_login(driver, usuario, senha)
clicar_agora_nao(driver)
clicar_meu_perfil(driver)
clicar_seguindo(driver)
deixar_de_seguir_perfis(driver, lote=10)  # Unfollow em lotes
```

## Notas de Desenvolvimento

- **Tratamento de erros**: Sistema robusto de exception handling
- **Reutilizacao de codigo**: Funcoes modulares e reutilizaveis
- **Documentacao**: Codigo bem comentado e documentado
- **Testes**: Validacao em diferentes cenarios

## Status do Projeto

- Extração de seguidores
- Interacao com reels
- Sistema de unfollow inteligente
- Pausas humanizadas
- Sistema de logging
- Tratamento de erros

---

**AVISO**: Use este bot de forma responsavel e respeite os termos de servico do Instagram. O desenvolvedor nao se responsabiliza por uso indevido.
