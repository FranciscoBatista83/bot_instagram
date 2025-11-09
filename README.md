# 🤖 Bot Instagram - Automação Completa

Bot automatizado para Instagram com múltiplas funcionalidades: extração de seguidores, interação com reels, visita de perfis e sistema de unfollow inteligente.

## 📋 Funcionalidades

### ✅ **Implementadas**

1. **🔍 Extração Inteligente de Seguidores**
   - Filtra apenas perfis de usuários reais
   - Lista negra de termos para URLs inválidas
   - Validação rigorosa de usernames (3-30 caracteres)

2. **👥 Visitação de Perfis**
   - Visita perfis aleatoriamente do arquivo `seguidores.txt`
   - Visita perfis específicos por URL
   - Verificação de carregamento do perfil

3. **🎬 Interação com Reels**
   - Encontra e acessa o primeiro reel de cada perfil
   - Verifica estado de curtida (coração preenchido vs vazio)
   - Curte automaticamente apenas se necessário
   - Processa todos os perfis em ordem sequencial

4. **🚫 Sistema de Unfollow Inteligente**
   - Deixa de seguir perfis em lotes controlados
   - Pausas de 15-30 minutos entre lotes
   - Evita detecção por comportamento robótico
   - Loop automático até completar todos os perfis

5. **⏱️ Sistema de Pausas Humanizadas**
   - Todas as pausas usam funções centralizadas do `utils.py`
   - Variações aleatórias para simular comportamento humano
   - Múltiplos tipos de pausa (curta, média, longa)

## 📁 Estrutura do Projeto

```
bot_instagram/
├── bots/
│   ├── __init__.py
│   ├── acessar_seguidores.py      # Extração de seguidores
│   ├── curtir_reels.py           # Interação com reels
│   └── deixar_de_seguir.py       # Sistema de unfollow
├── core/
│   ├── __init__.py
│   ├── actions.py                # Funções principais de automação
│   ├── browser.py                # Gerenciamento do navegador
│   └── file_manager.py           # Gerenciamento de arquivos
├── logger.py                     # Sistema de logging
├── utils.py                      # Funções utilitárias e pausas
├── requirements.txt              # Dependências Python
├── .env                          # Credenciais (não versionado)
├── seguidores.txt                # Lista de perfis extraídos
└── README.md                     # Esta documentação
```

## 🚀 Como Usar

### 1. **Instalação**

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd bot_instagram

# Instale as dependências
pip install -r requirements.txt
```

### 2. **Configuração**

Configure suas credenciais no arquivo `.env`:
```env
INSTAGRAM_USER=seu_usuario_aqui
INSTAGRAM_PASSWORD=sua_senha_aqui
```

### 3. **Execução dos Bots**

#### **🔍 Extrair Seguidores:**
```bash
python bots/acessar_seguidores.py
```

#### **🎬 Curtir Reels:**
```bash
python bots/curtir_reels.py
```

#### **🚫 Deixar de Seguir Perfis:**
```bash
python bots/deixar_de_seguir.py
```

## 📊 Detalhes das Funcionalidades

### **Sistema de Unfollow Inteligente**
- **Lotes configuráveis**: Padrão 10 perfis por lote
- **Pausas inteligentes**: 15-30 minutos entre lotes
- **Loop automático**: Continua até completar todos os perfis
- **Scroll automático**: Carrega mais perfis conforme necessário

**Exemplo de execução:**
```
=== LOTE 1 - Buscando perfis para deixar de seguir ===
Encontrados 25 perfis disponíveis no lote 1.
Lote 1 concluído: 10 perfis deixados de seguir.
⏰ Aguardando 15-30 minutos antes do próximo lote...
=== LOTE 2 - Buscando perfis para deixar de seguir ===
Encontrados 15 perfis disponíveis no lote 2.
Lote 2 concluído: 10 perfis deixados de seguir.
🎉 Processo de unfollow completamente concluído! Total: 20 perfis.
```

### **Interação com Reels**
- **Processamento sequencial**: Todos os perfis em ordem
- **Detecção inteligente**: Múltiplos métodos para encontrar reels
- **Verificação de estado**: Só curte se necessário
- **Relatório visual**: ✓ (curtido) / ○ (já curtido)

### **Extração de Seguidores**
- **Filtragem avançada**: Remove elementos da interface
- **Lista negra**: 15+ termos filtrados
- **Validação**: Usernames válidos apenas

## 🔧 Melhorias Técnicas

### **Sistema de Pausas Centralizado**
```python
# Exemplo de uso das pausas
pausa(min_tempo=2.0, max_tempo=5.0, jitter=0.3, nome="carregar página")
```

### **Lista Negra de Filtragem**
```python
blacklist_terms = [
    'accounts', 'archive', 'explore', 'web', 'reels', 'direct',
    'legal', 'privacy', 'terms', 'help', 'about', 'blog',
    'jobs', 'api', 'developer', 'press', 'advertising'
]
```

### **Verificação Inteligente de Curtidas**
- Análise do atributo `fill` do SVG
- Verificação de classes do elemento pai
- Múltiplos métodos de fallback

## � Logs e Monitoramento

O sistema gera logs detalhados em `bot.log` incluindo:
- ✅ Status de cada operação
- 👤 Perfis processados
- ⚠️ Warnings e erros
- 📊 Estatísticas finais

## 🔒 Segurança e Ética

- **🚫 Modo incógnito** ativado
- **⏱️ Pausas humanizadas** para evitar detecção
- **📏 Limitação de ações** por lote
- **🛡️ Tratamento robusto** de erros
- **⚖️ Uso responsável** - respeite os termos do Instagram

## 🛠️ Dependências

```txt
selenium>=4.15.0          # Automação web
python-dotenv>=1.0.0      # Gerenciamento de variáveis de ambiente
webdriver-manager>=4.0.0  # Gerenciamento automático de drivers
requests>=2.31.0          # Requisições HTTP
urllib3>=2.0.0           # Cliente HTTP
certifi>=2023.7.22       # Certificados SSL
charset-normalizer>=3.2.0 # Codificação de caracteres
idna>=3.4                # Internacionalização de domínios
```

## 🎯 Exemplo de Uso Programático

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

## 📝 Notas de Desenvolvimento

- **🐛 Tratamento de erros**: Sistema robusto de exception handling
- **🔄 Reutilização de código**: Funções modulares e reutilizáveis
- **📖 Documentação**: Código bem comentado e documentado
- **🧪 Testes**: Validação em diferentes cenários

## 🚧 Status do Projeto

- ✅ Extração de seguidores
- ✅ Interação com reels
- ✅ Sistema de unfollow inteligente
- ✅ Pausas humanizadas
- ✅ Sistema de logging
- ✅ Tratamento de erros

---

**⚠️ AVISO**: Use este bot de forma responsável e respeite os termos de serviço do Instagram. O desenvolvedor não se responsabiliza por uso indevido.
