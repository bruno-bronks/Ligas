# ⚙️ Configuração do App Android

## Escolha: Java ou Kotlin?

O projeto inclui duas versões do `MainActivity`:

- **Java**: `MainActivity.java` (padrão, já configurado)
- **Kotlin**: `MainActivity.kt` (alternativa moderna)

### Para usar Java (padrão):
✅ Nada a fazer - já está configurado!

### Para usar Kotlin:
1. Remova ou renomeie `MainActivity.java`
2. Descomente as linhas Kotlin em `app/build.gradle`:
   ```gradle
   plugins {
       id 'com.android.application'
       id 'org.jetbrains.kotlin.android' version '1.9.20'
   }
   
   kotlinOptions {
       jvmTarget = '1.8'
   }
   ```
3. Adicione a dependência Kotlin:
   ```gradle
   dependencies {
       implementation 'org.jetbrains.kotlin:kotlin-stdlib:1.9.20'
       // ... outras dependências
   }
   ```

## Configurar URL do Streamlit

Edite o arquivo `MainActivity` (Java ou Kotlin) e altere:

```java
// Java
private static final String STREAMLIT_URL = "https://seu-app.streamlit.app";
```

```kotlin
// Kotlin
private val streamlitUrl = "https://seu-app.streamlit.app"
```

### URLs para diferentes cenários:

| Cenário | URL |
|---------|-----|
| Streamlit Cloud | `https://seu-app.streamlit.app` |
| Emulador Android | `http://10.0.2.2:8501` |
| Dispositivo físico (mesma rede) | `http://192.168.1.X:8501` |
| Servidor com HTTPS | `https://seu-dominio.com` |

## Personalizar App

### Nome do App
Edite: `app/src/main/res/values/strings.xml`
```xml
<string name="app_name">Futebol Ligas</string>
```

### Package Name (ID do App)
Edite: `app/build.gradle`
```gradle
defaultConfig {
    applicationId "com.ligas.football"  // Mude aqui
    // ...
}
```

E também atualize em:
- `AndroidManifest.xml` (package)
- Estrutura de pastas Java/Kotlin

### Versão do App
Edite: `app/build.gradle`
```gradle
defaultConfig {
    versionCode 1        // Incremente a cada release
    versionName "1.0.0"  // Versão visível ao usuário
}
```

### Ícone do App
1. Gere ícones em: https://www.appicon.co/
2. Ou use Android Studio: `File > New > Image Asset`
3. Substitua arquivos em `app/src/main/res/mipmap-*/`

## Configurações de Build

### Min SDK (versão mínima do Android)
Edite: `app/build.gradle`
```gradle
minSdk 24  // Android 7.0 (Nougat)
```

### Target SDK (versão alvo)
```gradle
targetSdk 34  // Android 14
```

## Permissões

As permissões já estão configuradas no `AndroidManifest.xml`:
- ✅ Internet
- ✅ Network State

Para produção com HTTPS, remova:
```xml
android:usesCleartextTraffic="true"
```

## ProGuard (Obfuscação)

Para release, você pode habilitar minificação:
```gradle
buildTypes {
    release {
        minifyEnabled true  // Mude para true
        shrinkResources true
        // ...
    }
}
```

## Assinatura (Keystore)

Para gerar APK assinado para produção:

1. Gere keystore:
```bash
keytool -genkey -v -keystore ligas-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias ligas
```

2. Crie `app/keystore.properties`:
```properties
storePassword=sua_senha
keyPassword=sua_senha
keyAlias=ligas
storeFile=../ligas-release-key.jks
```

3. Adicione em `app/build.gradle`:
```gradle
android {
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
            // ...
        }
    }
}
```

## Variáveis de Ambiente

Para diferentes URLs por ambiente, use `buildConfigField`:

```gradle
android {
    buildTypes {
        debug {
            buildConfigField "String", "STREAMLIT_URL", '"http://10.0.2.2:8501"'
        }
        release {
            buildConfigField "String", "STREAMLIT_URL", '"https://seu-app.streamlit.app"'
        }
    }
}
```

E use no código:
```java
webView.loadUrl(BuildConfig.STREAMLIT_URL);
```


