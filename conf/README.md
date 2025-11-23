# Configuração de Múltiplos MCP Servers via Docker

## 📦 Arquivos Criados

1. **`conf/mcp-servers.json`** - Configuração JSON de todos os servidores MCP
2. **`conf/MCP_SERVERS_GUIDE.md`** - Documentação completa e guia de uso
3. **`mcp-servers.sh`** - Script bash para gerenciar servidores Docker

## 🚀 Quick Start

### 1. Tornar o script executável
```bash
chmod +x mcp-servers.sh
```

### 2. Baixar as imagens Docker
```bash
./mcp-servers.sh pull
```

### 3. Listar servidores disponíveis
```bash
./mcp-servers.sh list
```

### 4. Testar um servidor
```bash
./mcp-servers.sh test fetch
```

## 📚 Servidores Configurados

Os seguintes servidores MCP foram configurados no `conf/mcp-servers.json`:

| Servidor | Imagem | Descrição |
|----------|--------|-----------|
| **fetch** | `mcp/fetch` | Web content fetching e conversão para Markdown |
| **filesystem** | `mcp/filesystem` | Operações seguras em arquivos |
| **memory** | `mcp/memory` | Knowledge graph persistente |
| **git** | `mcp/git` | Operações em repositórios Git |
| **time** | `mcp/time` | Utilitários de tempo e timezone |

## ⚠️ Pontos Importantes

### 1. **Comunicação via stdio, NÃO via TCP**

Ao contrário do que eu havia sugerido inicialmente sobre usar portas TCP, **os servidores MCP via Docker usam `stdio` (stdin/stdout)** para comunicação. O Docker executa os containers em modo interativo (`-i`) e se comunica via pipes.

**NÃO há portas TCP envolvidas!**

### 2. **Montagem de Volumes**

Para servidores que precisam acessar o filesystem do host (filesystem, git), os diretórios são montados via Docker:

```bash
--mount type=bind,src=/host/path,dst=/container/path
```

Exemplos configurados:
- Filesystem: `/Users/joao/dev/NIE` → `/projects/NIE`
- Git: `/Users/joao/dev` → `/repos`

### 3. **Volume Persistente para Memory**

O Memory Server usa um volume Docker para persistir dados:

```bash
docker volume create mcp-client-memory
```

## 🔧 Comandos Úteis

```bash
# Ver informações dos servidores
./mcp-servers.sh info

# Listar imagens instaladas
./mcp-servers.sh list

# Baixar todas as imagens
./mcp-servers.sh pull

# Construir localmente (se necessário)
./mcp-servers.sh build

# Testar servidor específico
./mcp-servers.sh test fetch
./mcp-servers.sh test filesystem
./mcp-servers.sh test memory

# Limpar tudo
./mcp-servers.sh clean
```

## 📖 Próximos Passos

Para **implementar suporte a múltiplos servidores** no `mcp-client`, será necessário:

1. **Modificar `cli.py`** para adicionar opção `--server <name>`
2. **Criar função de carregamento** do `conf/mcp-servers.json`
3. **Modificar `MCPClient`** para aceitar configuração de servidor do JSON
4. **Adicionar comando** `--list-servers` para listar servidores disponíveis

### Exemplo de uso futuro:

```bash
# Listar servidores configurados
python3 -m mcp_client --list-servers

# Usar servidor específico
python3 -m mcp_client --server fetch --chat
python3 -m mcp_client --server filesystem --chat
python3 -m mcp_client --server memory --chat --provider ollama
```

## 📝 Documentação Completa

Para informações detalhadas sobre cada servidor, configurações, segurança e troubleshooting, consulte:

**`conf/MCP_SERVERS_GUIDE.md`**

## 🔗 Links Úteis

- **Repositório oficial MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Documentação MCP**: https://modelcontextprotocol.io
- **Docker Hub**: https://hub.docker.com

---

**Nota**: Esta configuração prepara o ambiente para uso de múltiplos servidores MCP via Docker. A implementação completa no código do `mcp-client` ainda precisa ser desenvolvida seguindo os "Próximos Passos" descritos acima.
