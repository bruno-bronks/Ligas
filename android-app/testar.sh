#!/bin/bash
# Script para facilitar testes do app Android

echo "🧪 Script de Teste - App Android Futebol Ligas"
echo "=============================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar se Streamlit está rodando
check_streamlit() {
    echo -e "${YELLOW}Verificando se Streamlit está rodando...${NC}"
    if curl -s http://localhost:8501 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Streamlit está rodando em http://localhost:8501${NC}"
        return 0
    else
        echo -e "${RED}❌ Streamlit não está rodando${NC}"
        echo "Execute: streamlit run streamlit_app.py"
        return 1
    fi
}

# Verificar se dispositivo está conectado
check_device() {
    echo -e "${YELLOW}Verificando dispositivos conectados...${NC}"
    if command_exists adb; then
        DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)
        if [ "$DEVICES" -gt 0 ]; then
            echo -e "${GREEN}✅ $DEVICES dispositivo(s) conectado(s)${NC}"
            adb devices
            return 0
        else
            echo -e "${YELLOW}⚠️  Nenhum dispositivo conectado${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  ADB não encontrado (Android SDK não configurado?)${NC}"
        return 1
    fi
}

# Obter IP local
get_local_ip() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        ip addr show | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | cut -d/ -f1 | head -1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        ipconfig | grep "IPv4" | awk '{print $14}' | head -1
    fi
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) Verificar ambiente (Streamlit, dispositivos)"
    echo "2) Obter IP local (para dispositivo físico)"
    echo "3) Compilar APK de debug"
    echo "4) Instalar APK no dispositivo"
    echo "5) Executar app (via Android Studio/Gradle)"
    echo "6) Limpar projeto"
    echo "7) Sair"
    echo ""
    read -p "Opção: " choice
}

# Executar opção escolhida
case "$1" in
    check)
        check_streamlit
        check_device
        ;;
    ip)
        IP=$(get_local_ip)
        echo -e "${GREEN}IP local: $IP${NC}"
        echo "Configure no MainActivity.java: http://$IP:8501"
        ;;
    build)
        echo -e "${YELLOW}Compilando APK de debug...${NC}"
        ./gradlew assembleDebug
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ APK gerado em: app/build/outputs/apk/debug/app-debug.apk${NC}"
        fi
        ;;
    install)
        if check_device; then
            echo -e "${YELLOW}Instalando APK...${NC}"
            adb install -r app/build/outputs/apk/debug/app-debug.apk
        else
            echo -e "${RED}❌ Conecte um dispositivo primeiro${NC}"
        fi
        ;;
    run)
        echo -e "${YELLOW}Executando app...${NC}"
        ./gradlew installDebug
        adb shell am start -n com.ligas.football/.MainActivity
        ;;
    clean)
        echo -e "${YELLOW}Limpando projeto...${NC}"
        ./gradlew clean
        ;;
    *)
        # Menu interativo
        while true; do
            show_menu
            case $choice in
                1)
                    check_streamlit
                    check_device
                    ;;
                2)
                    IP=$(get_local_ip)
                    echo -e "${GREEN}IP local: $IP${NC}"
                    echo "Configure no MainActivity.java: http://$IP:8501"
                    ;;
                3)
                    echo -e "${YELLOW}Compilando APK de debug...${NC}"
                    ./gradlew assembleDebug
                    ;;
                4)
                    if check_device; then
                        echo -e "${YELLOW}Instalando APK...${NC}"
                        adb install -r app/build/outputs/apk/debug/app-debug.apk
                    fi
                    ;;
                5)
                    if check_device; then
                        echo -e "${YELLOW}Instalando e executando app...${NC}"
                        ./gradlew installDebug
                        adb shell am start -n com.ligas.football/.MainActivity
                    fi
                    ;;
                6)
                    echo -e "${YELLOW}Limpando projeto...${NC}"
                    ./gradlew clean
                    ;;
                7)
                    echo "Até logo!"
                    exit 0
                    ;;
                *)
                    echo -e "${RED}Opção inválida${NC}"
                    ;;
            esac
        done
        ;;
esac

