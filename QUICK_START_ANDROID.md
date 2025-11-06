
# 🚀 Guia Rápido - App Android

## Passos Rápidos para Começar

### 1️⃣ Hospedar o App (Escolha uma opção)

#### Opção A: Node.js Local (Recomendado para testes)
```bash
cd nodejs-app
npm install
# Crie .env com FOOTBALL_DATA_API_KEY
npm start
```
Servidor em: `http://localhost:3000`

#### Opção B: Node.js em Produção
- Heroku, Railway, VPS, etc.
- Veja `nodejs-app/README.md` para deploy

#### Opção C: Streamlit (Legado)
```bash
streamlit run streamlit_app.py --server.port 8501
```

### 2️⃣ Configurar o App Android

1. Abra `android-app/app/src/main/java/com/ligas/football/MainActivity.java`
2. Altere a linha:
   ```java
   private static final String APP_URL = "http://10.0.2.2:3000";
   ```
   - **Emulador**: `http://10.0.2.2:3000` (Node.js) ou `http://10.0.2.2:8501` (Streamlit)
   - **Dispositivo físico**: `http://IP_DO_COMPUTADOR:3000`
   - **Produção**: `https://seu-servidor.com`

### 3️⃣ Abrir no Android Studio

1. Instale o [Android Studio](https://developer.android.com/studio)
2. Abra: `File > Open` → Selecione a pasta `android-app`
3. Aguarde o Gradle sincronizar

### 4️⃣ Configurar SDK

1. `File > Settings > Android SDK`
2. Instale:
   - Android SDK Platform 34
   - Android SDK Build-Tools
   - Android Emulator (se não tiver dispositivo físico)

### 5️⃣ Criar local.properties

Crie o arquivo `android-app/local.properties`:
```properties
sdk.dir=C\:\\Users\\SeuUsuario\\AppData\\Local\\Android\\Sdk
```
*(Substitua pelo caminho do seu SDK)*

### 6️⃣ Executar

1. Conecte um dispositivo Android OU inicie um emulador
2. Clique no botão ▶️ Run ou pressione `Shift+F10`

## 📦 Gerar APK para Instalar

### APK de Debug (Testes)
```bash
cd android-app
./gradlew assembleDebug
```
APK em: `app/build/outputs/apk/debug/app-debug.apk`

### Instalar no Dispositivo
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

## 🔧 URLs Comuns

- **Node.js local (emulador)**: `http://10.0.2.2:3000`
- **Node.js local (dispositivo)**: `http://192.168.1.X:3000`
- **Streamlit local (emulador)**: `http://10.0.2.2:8501`
- **Produção**: `https://seu-servidor.com`

## ⚠️ Problemas Comuns

**App não carrega?**
- Verifique se o servidor (Node.js ou Streamlit) está rodando
- Verifique a URL em `MainActivity.java`
- Para emulador, use `10.0.2.2` (não `localhost`)
- Teste a URL no navegador do dispositivo primeiro

**Erro de compilação?**
- Sincronize: `File > Sync Project with Gradle Files`
- Limpe: `Build > Clean Project`

**Mais ajuda?**
- Veja `README_ANDROID.md` para documentação completa do Android
- Veja `nodejs-app/COMO_TESTAR.md` para testar o Node.js
- Veja `android-app/COMO_TESTAR.md` para testar o app Android


