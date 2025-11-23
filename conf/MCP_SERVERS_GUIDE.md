# Guia de Configuração: MCP Servers via Docker

## 📋 Visão Geral

Este documento explica como usar múltiplos MCP Servers via Docker com o `mcp-client`. Todos os servidores oficiais estão disponíveis como imagens Docker pré-construídas.

## 🐳 Pré-requisitos

1. **Docker instalado e rodando**:
   ```bash
   docker --version  # Deve ser >= 20.10.0
   docker ps         # Verifica se o Docker está rodando
   ```

2. **Baixar as imagens Docker dos servidores MCP**:
   ```bash
   # Fetch Server - Web content fetching
   docker pull mcp/fetch
   
   # Filesystem Server - File operations
   docker pull mcp/filesystem
   
   # Memory Server - Persistent knowledge graph
   docker pull mcp/memory
   
   # Git Server - Git operations
   docker pull mcp/git
   
   # Time Server - Time and timezone utilities
   docker pull mcp/time
   ```

3. **Criar volume Docker para o Memory Server**:
   ```bash
   docker volume create mcp-client-memory
   ```

## 📁 Arquivo de Configuração

O arquivo `conf/mcp-servers.json` contém a configuração de todos os servidores MCP disponíveis. Cada servidor é executado via Docker com comunicação via `stdio` (stdin/stdout).

### ⚠️ IMPORTANTE: Não use TCP/Portas

**Os servidores MCP via Docker NÃO usam portas TCP!** Eles usam `stdio` (stdin/stdout) para comunicação. O Docker executa o container em modo interativo (`-i`) e se comunica via pipes.

## 🔧 Servidores Disponíveis

### 1. **Fetch Server** - Web Content Fetching

**Função**: Busca conteúdo web e converte para Markdown.

**Imagem Docker**: `mcp/fetch`

**Uso**:
```bash
python3 -m mcp_client --server fetch --chat
```

**Ferramentas disponíveis**:
- `fetch(url, max_length, raw)` - Busca URL e extrai conteúdo

**Segurança**: ⚠️ Pode acessar IPs locais/internos - use com cautela!

**Customização**:
```json
{
  "args": [
    "run", "-i", "--rm", "mcp/fetch",
    "--ignore-robots-txt",  // Ignora robots.txt
    "--user-agent=CustomAgent"  // User-agent customizado
  ]
}
```

---

### 2. **Filesystem Server** - File Operations

**Função**: Operações seguras em arquivos com controle de acesso.

**Imagem Docker**: `mcp/filesystem`

**Uso**:
```bash
python3 -m mcp_client --server filesystem --chat
```

**Ferramentas disponíveis**:
- `read_file` - Lê arquivo
- `write_file` - Escreve arquivo
- `edit_file` - Edita arquivo
- `create_directory` - Cria diretório
- `list_directory` - Lista diretório
- `move_file` - Move/renomeia arquivo
- `search_files` - Busca arquivos
- `get_file_info` - Info do arquivo

**Diretórios montados** (configurados em `mcp-servers.json`):
- `/Users/joao/dev/NIE` → `/projects/NIE` (leitura/escrita)
- `/Users/joao/Documents` → `/projects/Documents` (somente leitura)

**Customização**: Edite `mounted_directories` no JSON para adicionar/remover diretórios.

---

### 3. **Memory Server** - Knowledge Graph

**Função**: Memória persistente usando grafo de conhecimento.

**Imagem Docker**: `mcp/memory`

**Uso**:
```bash
python3 -m mcp_client --server memory --chat
```

**Ferramentas disponíveis**:
- `create_entities` - Cria entidades
- `create_relations` - Cria relações
- `add_observations` - Adiciona observações
- `delete_entities` - Remove entidades
- `read_graph` - Lê grafo
- `search_nodes` - Busca nós
- `open_nodes` - Abre nós

**Volume Docker**: `mcp-client-memory` (persiste dados entre sessões)

**Estrutura de dados**:
```json
{
  "entityName": "João_Parana",
  "observations": [
    "Trabalha com Python e Java",
    "Usa MacBook M3",
    "Desenvolve projetos de pesquisa em NIE"
  ]
}
```

---

### 4. **Git Server** - Git Operations

**Função**: Operações em repositórios Git.

**Imagem Docker**: `mcp/git`

**Uso**:
```bash
python3 -m mcp_client --server git --chat
```

**Ferramentas disponíveis**:
- `git_status` - Status do repo
- `git_diff` - Diferenças
- `git_commit` - Commit
- `git_log` - Histórico
- `git_show` - Mostra commit
- `git_search` - Busca no código
- `git_blame` - Autor das linhas

**Diretório montado**:
- `/Users/joao/dev` → `/repos` (leitura/escrita)

---

### 5. **Time Server** - Time Utilities

**Função**: Utilitários de tempo e timezone.

**Imagem Docker**: `mcp/time`

**Uso**:
```bash
python3 -m mcp_client --server time --chat
```

**Ferramentas disponíveis**:
- `get_current_time` - Hora atual
- `convert_time` - Converte entre timezones
- `get_timezone_info` - Info de timezone

---

## 🚀 Como Usar

### Método 1: Especificar servidor na linha de comando (FUTURO)

```bash
# Listar servidores disponíveis
python3 -m mcp_client --list-servers

# Usar servidor específico
python3 -m mcp_client --server fetch --chat
python3 -m mcp_client --server filesystem --chat
python3 -m mcp_client --server memory --chat
```

### Método 2: Usar servidor diretamente (ATUAL)

```bash
# Como o suporte a múltiplos servers ainda não está implementado,
# você pode testar cada servidor individualmente criando um wrapper:

# Exemplo para Fetch Server:
docker run -i --rm mcp/fetch
```

## 🔨 Construindo Servidores a partir do Fonte

Se quiser construir as imagens Docker localmente:

```bash
# 1. Clone o repositório oficial
git clone https://github.com/modelcontextprotocol/servers.git
cd servers

# 2. Construa as imagens
docker build -t mcp/fetch -f src/fetch/Dockerfile .
docker build -t mcp/filesystem -f src/filesystem/Dockerfile .
docker build -t mcp/memory -f src/memory/Dockerfile .
docker build -t mcp/git -f src/git/Dockerfile .
docker build -t mcp/time -f src/time/Dockerfile .
```

## 🔐 Notas de Segurança

1. **Fetch Server**: Pode acessar IPs locais/internos - cuidado em redes internas!
2. **Filesystem Server**: Acesso limitado apenas aos diretórios montados
3. **Memory Server**: Dados armazenados em volume Docker `mcp-client-memory`
4. **Git Server**: Acesso aos repositórios montados - pode fazer commits!
5. **Time Server**: Sem riscos de segurança

## 🐛 Troubleshooting

### Erro: "Cannot connect to Docker daemon"
```bash
# Inicie o Docker Desktop (macOS) ou Docker daemon (Linux)
open -a Docker  # macOS
```

### Erro: "Image not found: mcp/fetch"
```bash
# Baixe a imagem
docker pull mcp/fetch
```

### Erro: Memory Server não persiste dados
```bash
# Verifique se o volume existe
docker volume ls | grep mcp-client-memory

# Crie o volume se necessário
docker volume create mcp-client-memory
```

### Filesystem Server não acessa diretórios
```bash
# Verifique os mounts no mcp-servers.json
# Certifique-se que os caminhos do host existem:
ls -la /Users/joao/dev/NIE
ls -la /Users/joao/Documents
```

## 📚 Recursos Adicionais

- **Repositório oficial MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Documentação MCP**: https://modelcontextprotocol.io
- **Docker Hub (se disponível)**: https://hub.docker.com/u/mcp

## 🎯 Próximos Passos para Implementação

Para suportar múltiplos servidores no `mcp-client`, será necessário:

1. **Carregar configuração** do `conf/mcp-servers.json`
2. **Adicionar CLI option** `--server <name>` para selecionar servidor
3. **Adicionar comando** `--list-servers` para listar disponíveis
4. **Modificar `MCPClient`** para aceitar configuração de servidor
5. **Implementar seleção dinâmica** de servidor baseada no JSON

Exemplo de implementação futura:

```python
# cli.py
parser.add_argument(
    '--server',
    choices=['fetch', 'filesystem', 'memory', 'git', 'time'],
    help='Nome do servidor MCP a usar (configurado em conf/mcp-servers.json)'
)

parser.add_argument(
    '--list-servers',
    action='store_true',
    help='Lista servidores MCP disponíveis'
)
```

---

**Nota**: Este arquivo descreve a configuração e uso **pretendido**. A implementação completa do suporte a múltiplos servidores via arquivo de configuração ainda precisa ser desenvolvida no código do `mcp-client`.
