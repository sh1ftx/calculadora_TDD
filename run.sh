#!/bin/bash
set -e

#############################################
# CONFIGURAÇÕES
#############################################
PROJECT_NAME="calculadora_tdd"
VENV_DIR="venv"
PYTHON_BIN="python3"

#############################################
# CORES (ANSI)
#############################################
RED="\033[1;31m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;36m"
WHITE="\033[0;37m"
RESET="\033[0m"

#############################################
# FUNÇÕES AUXILIARES
#############################################
typewriter() {
    local text="$1"
    local delay="${2:-0.015}"
    for ((i=0; i<${#text}; i++)); do
        printf "%s" "${text:$i:1}"
        sleep "$delay"
    done
    printf "\n"
}

section() {
    echo -e "${BLUE}"
    echo "=============================================================="
    echo " $1"
    echo "=============================================================="
    echo -e "${RESET}"
}

#############################################
# INÍCIO
#############################################
clear

section "EXECUÇÃO DO PROJETO — CICLO TDD (Test Driven Development)"

typewriter "O shell é o orquestrador."
typewriter "Os scripts Python executam cada fase do TDD."
echo

typewriter "Fases:"
echo -e "  ${RED}🔴 RED${RESET}      → definição do comportamento"
echo -e "  ${GREEN}🟢 GREEN${RESET}    → implementação mínima"
echo -e "  ${YELLOW}♻️  REFACTOR${RESET} → melhoria segura"
echo
sleep 1

#############################################
# DETECÇÃO DE SISTEMA
#############################################
typewriter "🔍 Detectando sistema operacional..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS="$ID"
else
    echo -e "${RED}❌ Não foi possível detectar o sistema.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ Sistema detectado: $OS${RESET}"
sleep 1

#############################################
# INSTALAÇÃO DO PYTHON
#############################################
install_arch() {
    sudo pacman -Sy --noconfirm python python-pip python-virtualenv
}

install_debian() {
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
}

case "$OS" in
    arch|manjaro)
        install_arch
        PYTHON_BIN="python"
        ;;
    ubuntu|debian|linuxmint|pop)
        install_debian
        PYTHON_BIN="python3"
        ;;
    *)
        echo -e "${RED}❌ Distro não suportada automaticamente.${RESET}"
        exit 1
        ;;
esac

#############################################
# AMBIENTE VIRTUAL
#############################################
section "PREPARANDO AMBIENTE PYTHON"

if [ ! -d "$VENV_DIR" ]; then
    typewriter "🐍 Criando ambiente virtual..."
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

typewriter "⚡ Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

typewriter "⬆ Atualizando pip..."
pip install --quiet --upgrade pip

if [ -f requirements.txt ]; then
    typewriter "📦 Instalando dependências..."
    pip install --quiet -r requirements.txt
else
    echo -e "${YELLOW}⚠️ requirements.txt não encontrado.${RESET}"
fi

sleep 1

#############################################
# EXECUÇÃO DO CICLO TDD
#############################################
section "▶ INICIANDO CICLO TDD REAL (RED → GREEN → REFACTOR)"

typewriter "Agora o controle passa para o Python."
typewriter "Cada fase será executada, explicada e validada em tempo real."
echo
sleep 1

#############################################
# EXECUTA O RUNNER PYTHON (RICH)
#############################################
python tdd_runner.py

#############################################
# FINAL
#############################################
section "EXECUÇÃO FINALIZADA"

echo -e "${GREEN}✅ Projeto executado com sucesso.${RESET}"
echo -e "${BLUE}✔ TDD real executado corretamente.${RESET}"
echo
