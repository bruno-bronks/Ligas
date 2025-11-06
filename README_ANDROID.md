# 📱 App Android - Futebol Ligas

Este diretório contém o código-fonte do aplicativo Android que carrega o dashboard Streamlit em um WebView.

## 🚀 Como Funciona

O app Android é um wrapper que carrega seu app Streamlit em um WebView nativo. Isso permite:
- Interface nativa Android
- Funciona offline (se configurado)
- Melhor performance
- Acesso a recursos do dispositivo

## 📋 Pré-requisitos

1. **Android Studio** (versão mais recente recomendada)
   - Download: https://developer.android.com/studio

2. **SDK Android** (mínimo API 24 - Android 7.0)
   - Instalado via Android Studio SDK Manager

3. **App Streamlit hospedado**
   - Opção 1: Streamlit Cloud (gratuito) - https://streamlit.io/cloud
   - Opção 2: Servidor próprio (Heroku, AWS, etc.)
   - Opção 3: Para testes locais, use o emulador Android

## 🔧 Configuração

### 1. Configurar a URL do Streamlit

Edite o arquivo `app/src/main/java/com/ligas/football/MainActivity.java`:

```java
// Para Streamlit Cloud:
private static final String STREAMLIT_URL = "https://seu-app.streamlit.app";

// Para desenvolvimento local (Android Emulator):
private static final String STREAMLIT_URL = "http://10.0.2.2:8501";

// Para dispositivo físico na mesma rede:
private static final String STREAMLIT_URL = "http://192.168.1.X:8501";
```

### 2. Configurar SDK do Android

1. Abra o Android Studio
2. Vá em `File > Settings > Appearance & Behavior > System Settings > Android SDK`
3. Instale o SDK Platform para API 34 (ou a versão desejada)
4. Instale o Android SDK Build-Tools

### 3. Configurar local.properties

Crie o arquivo `local.properties` na raiz do projeto `android-app/`:

```properties
sdk.dir=C\:\\Users\\SeuUsuario\\AppData\\Local\\Android\\Sdk
```

**Nota:** No Windows, use barras invertidas duplas (`\\`) ou barras normais (`/`).

## 🏗️ Como Compilar

### Opção 1: Android Studio (Recomendado)

1. Abra o Android Studio
2. Selecione `File > Open` e escolha a pasta `android-app`
3. Aguarde o Gradle sincronizar
4. Conecte um dispositivo Android ou inicie um emulador
5. Clique em `Run > Run 'app'` ou pressione `Shift+F10`

### Opção 2: Linha de Comando

```bash
cd android-app
./gradlew assembleDebug
```

O APK será gerado em: `app/build/outputs/apk/debug/app-debug.apk`

## 📦 Gerar APK para Distribuição

### APK de Debug (para testes)

```bash
cd android-app
./gradlew assembleDebug
```

### APK de Release (para produção)

1. Configure uma keystore (chave de assinatura):
```bash
keytool -genkey -v -keystore ligas-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias ligas
```

2. Crie o arquivo `app/keystore.properties`:
```properties
storePassword=sua_senha
keyPassword=sua_senha
keyAlias=ligas
storeFile=../ligas-release-key.jks
```

3. Atualize `app/build.gradle` para incluir a configuração de release:
```gradle
android {
    ...
    signingConfigs {
        release {
            def keystorePropertiesFile = rootProject.file("keystore.properties")
            def keystoreProperties = new Properties()
            keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
            
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

4. Compile o APK de release:
```bash
./gradlew assembleRelease
```

O APK estará em: `app/build/outputs/apk/release/app-release.apk`

## 🌐 Hospedar o Streamlit

### Opção 1: Streamlit Cloud (Mais Fácil)

1. Crie uma conta em https://streamlit.io/cloud
2. Conecte seu repositório GitHub
3. Configure o arquivo principal como `streamlit_app.py`
4. Adicione as variáveis de ambiente necessárias (ex: `FOOTBALL_DATA_API_KEY`)
5. Deploy automático!

### Opção 2: Servidor Próprio

1. Instale o Streamlit no servidor:
```bash
pip install streamlit
```

2. Execute o app:
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

3. Configure um proxy reverso (nginx) com SSL se necessário

## 📱 Testar no Dispositivo

### Emulador Android

1. No Android Studio: `Tools > Device Manager`
2. Crie um novo dispositivo virtual
3. Execute o app normalmente

### Dispositivo Físico

1. Ative as **Opções de Desenvolvedor** no seu Android:
   - Vá em `Configurações > Sobre o telefone`
   - Toque 7 vezes em "Número da versão"
   
2. Ative a **Depuração USB**:
   - `Configurações > Opções do desenvolvedor > Depuração USB`

3. Conecte via USB e autorize a depuração

4. Execute o app do Android Studio

## 🔒 Segurança

- O app usa `usesCleartextTraffic="true"` para permitir HTTP local
- Para produção, use HTTPS e remova essa permissão
- Configure CORS adequadamente no servidor Streamlit

## 🐛 Troubleshooting

### App não carrega a URL

- Verifique se o Streamlit está rodando
- Verifique a URL em `MainActivity.java`
- Para emulador, use `10.0.2.2` em vez de `localhost`
- Verifique as permissões de Internet no `AndroidManifest.xml`

### Erro de compilação

- Sincronize o projeto: `File > Sync Project with Gradle Files`
- Limpe o projeto: `Build > Clean Project`
- Reconstrua: `Build > Rebuild Project`

### WebView não funciona

- Verifique se o JavaScript está habilitado
- Verifique os logs: `Logcat` no Android Studio
- Teste a URL em um navegador primeiro

## 📝 Estrutura do Projeto

```
android-app/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/ligas/football/
│   │   │   │   └── MainActivity.java
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   │   └── activity_main.xml
│   │   │   │   ├── values/
│   │   │   │   │   ├── strings.xml
│   │   │   │   │   ├── colors.xml
│   │   │   │   │   └── themes.xml
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle
│   └── proguard-rules.pro
├── build.gradle
├── settings.gradle
└── gradle.properties
```

## 🎨 Personalização

### Mudar o ícone do app

1. Gere ícones em: https://www.appicon.co/ ou Android Studio
2. Substitua os arquivos em `app/src/main/res/mipmap-*/`

### Mudar o nome do app

Edite `app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Seu Nome Aqui</string>
```

### Adicionar Splash Screen

Crie uma tela de carregamento antes do WebView carregar.

## 📄 Licença

Mesma licença do projeto principal.

## 🤝 Suporte

Para problemas ou dúvidas, verifique:
- Logs do Android Studio (Logcat)
- Console do navegador (se acessar via browser)
- Documentação do Streamlit: https://docs.streamlit.io/


