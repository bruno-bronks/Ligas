@echo off
REM Script para facilitar testes do app Android (Windows)

echo 🧪 Script de Teste - App Android Futebol Ligas
echo ==============================================
echo.

REM Verificar se Streamlit está rodando
echo Verificando se Streamlit está rodando...
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Streamlit está rodando em http://localhost:8501
) else (
    echo ❌ Streamlit não está rodando
    echo Execute: streamlit run streamlit_app.py
)

echo.
echo Verificando dispositivos conectados...
adb devices

echo.
echo Escolha uma opção:
echo 1) Obter IP local (para dispositivo físico)
echo 2) Compilar APK de debug
echo 3) Instalar APK no dispositivo
echo 4) Executar app
echo 5) Limpar projeto
echo 6) Sair
echo.
set /p choice="Opção: "

if "%choice%"=="1" (
    echo.
    echo Obtendo IP local...
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
        set ip=%%a
        set ip=!ip:~1!
        echo IP local: !ip!
        echo Configure no MainActivity.java: http://!ip!:8501
        goto :end
    )
)

if "%choice%"=="2" (
    echo.
    echo Compilando APK de debug...
    call gradlew.bat assembleDebug
    if %errorlevel% equ 0 (
        echo ✅ APK gerado em: app\build\outputs\apk\debug\app-debug.apk
    )
)

if "%choice%"=="3" (
    echo.
    echo Instalando APK...
    adb install -r app\build\outputs\apk\debug\app-debug.apk
)

if "%choice%"=="4" (
    echo.
    echo Instalando e executando app...
    call gradlew.bat installDebug
    adb shell am start -n com.ligas.football/.MainActivity
)

if "%choice%"=="5" (
    echo.
    echo Limpando projeto...
    call gradlew.bat clean
)

if "%choice%"=="6" (
    echo Até logo!
    exit /b 0
)

:end
pause

