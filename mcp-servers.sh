#!/usr/bin/env bash
# MCP Servers Docker Management Script
# Gerencia servidores MCP via Docker

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Função para verificar se Docker está rodando
check_docker() {
    if ! docker info &> /dev/null; then
        print_color $RED "❌ Docker não está rodando!"
        print_color $YELLOW "Por favor, inicie o Docker Desktop (macOS) ou Docker daemon (Linux)"
        exit 1
    fi
}

# Função para listar imagens MCP
list_images() {
    print_color $BLUE "📦 Imagens MCP Docker disponíveis:"
    echo ""
    docker images | grep -E "^mcp/" || print_color $YELLOW "Nenhuma imagem MCP encontrada"
}

# Função para baixar todas as imagens
pull_all() {
    print_color $BLUE "⬇️  Baixando todas as imagens MCP oficiais..."
    echo ""
    
    local servers=("fetch" "filesystem" "memory" "git" "time")
    
    for server in "${servers[@]}"; do
        print_color $GREEN "Baixando mcp/$server..."
        if docker pull mcp/$server; then
            print_color $GREEN "✅ mcp/$server baixado com sucesso"
        else
            print_color $YELLOW "⚠️  mcp/$server não disponível no Docker Hub (pode precisar construir localmente)"
        fi
        echo ""
    done
    
    print_color $BLUE "Criando volume Docker para Memory Server..."
    docker volume create mcp-client-memory || print_color $YELLOW "Volume mcp-client-memory já existe"
}

# Função para construir imagens localmente
build_all() {
    print_color $BLUE "🔨 Construindo imagens MCP localmente..."
    echo ""
    
    if [ ! -d "../servers" ]; then
        print_color $YELLOW "Repositório oficial não encontrado. Clonando..."
        cd ..
        git clone https://github.com/modelcontextprotocol/servers.git
        cd servers
    else
        cd ../servers
    fi
    
    local servers=("fetch" "filesystem" "memory" "git" "time")
    
    for server in "${servers[@]}"; do
        if [ -f "src/$server/Dockerfile" ]; then
            print_color $GREEN "Construindo mcp/$server..."
            if docker build -t mcp/$server -f src/$server/Dockerfile .; then
                print_color $GREEN "✅ mcp/$server construído com sucesso"
            else
                print_color $RED "❌ Erro ao construir mcp/$server"
            fi
        else
            print_color $YELLOW "⚠️  Dockerfile não encontrado para $server"
        fi
        echo ""
    done
    
    cd - > /dev/null
    
    print_color $BLUE "Criando volume Docker para Memory Server..."
    docker volume create mcp-client-memory || print_color $YELLOW "Volume mcp-client-memory já existe"
}

# Função para remover imagens
clean() {
    print_color $YELLOW "🗑️  Removendo imagens MCP..."
    echo ""
    
    docker images | grep -E "^mcp/" | awk '{print $1":"$2}' | while read image; do
        print_color $YELLOW "Removendo $image..."
        docker rmi $image || true
    done
    
    print_color $BLUE "Remover volume de dados do Memory Server? (s/N)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        docker volume rm mcp-client-memory || print_color $YELLOW "Volume não existe"
    fi
}

# Função para testar um servidor
test_server() {
    local server=$1
    
    if [ -z "$server" ]; then
        print_color $RED "❌ Especifique o servidor a testar: fetch, filesystem, memory, git, time"
        exit 1
    fi
    
    print_color $BLUE "🧪 Testando servidor: $server"
    echo ""
    
    case $server in
        fetch)
            print_color $GREEN "Iniciando Fetch Server..."
            docker run -i --rm mcp/fetch
            ;;
        filesystem)
            print_color $GREEN "Iniciando Filesystem Server..."
            docker run -i --rm \
                --mount type=bind,src=/Users/joao/dev/NIE,dst=/projects/NIE \
                mcp/filesystem /projects
            ;;
        memory)
            print_color $GREEN "Iniciando Memory Server..."
            docker run -i -v mcp-client-memory:/app/dist --rm mcp/memory
            ;;
        git)
            print_color $GREEN "Iniciando Git Server..."
            docker run -i --rm \
                --mount type=bind,src=/Users/joao/dev,dst=/repos \
                mcp/git /repos
            ;;
        time)
            print_color $GREEN "Iniciando Time Server..."
            docker run -i --rm mcp/time
            ;;
        *)
            print_color $RED "❌ Servidor desconhecido: $server"
            print_color $YELLOW "Servidores disponíveis: fetch, filesystem, memory, git, time"
            exit 1
            ;;
    esac
}

# Função para mostrar informações
info() {
    print_color $BLUE "ℹ️  Informações sobre MCP Servers via Docker"
    echo ""
    print_color $GREEN "Configuração: conf/mcp-servers.json"
    print_color $GREEN "Documentação: conf/MCP_SERVERS_GUIDE.md"
    echo ""
    print_color $BLUE "Servidores disponíveis:"
    echo "  • fetch      - Web content fetching"
    echo "  • filesystem - File operations"
    echo "  • memory     - Knowledge graph"
    echo "  • git        - Git operations"
    echo "  • time       - Time utilities"
    echo ""
    print_color $BLUE "Volumes Docker:"
    docker volume ls | grep mcp || print_color $YELLOW "Nenhum volume MCP encontrado"
}

# Função para mostrar uso
usage() {
    cat << EOF
Uso: ./mcp-servers.sh [comando]

Comandos:
  pull        Baixa todas as imagens MCP oficiais do Docker Hub
  build       Constrói as imagens MCP localmente (requer clone do repositório oficial)
  list        Lista imagens MCP instaladas
  clean       Remove todas as imagens MCP e volumes
  test <srv>  Testa um servidor específico (fetch, filesystem, memory, git, time)
  info        Mostra informações sobre os servidores
  help        Mostra esta mensagem

Exemplos:
  ./mcp-servers.sh pull          # Baixa todas as imagens
  ./mcp-servers.sh build         # Constrói localmente
  ./mcp-servers.sh list          # Lista imagens instaladas
  ./mcp-servers.sh test fetch    # Testa o Fetch Server
  ./mcp-servers.sh info          # Informações gerais

EOF
}

# Main
main() {
    check_docker
    
    local command=${1:-help}
    
    case $command in
        pull)
            pull_all
            ;;
        build)
            build_all
            ;;
        list)
            list_images
            ;;
        clean)
            clean
            ;;
        test)
            test_server "$2"
            ;;
        info)
            info
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_color $RED "❌ Comando desconhecido: $command"
            echo ""
            usage
            exit 1
            ;;
    esac
}

main "$@"
