# 📱 App Android - Futebol Ligas Dashboard

Aplicativo Android nativo que carrega o dashboard Streamlit de futebol em um WebView.

## 🎯 O que é?

Este app é um wrapper Android que exibe seu dashboard Streamlit em uma interface nativa. Funciona como um navegador dedicado, mas com melhor integração ao sistema Android.

## 📁 Estrutura

```
android-app/
├── app/
│   ├── src/main/
│   │   ├── java/com/ligas/football/
│   │   │   ├── MainActivity.java    # Versão Java (padrão)
│   │   │   └── MainActivity.kt      # Versão Kotlin (opcional)
│   │   ├── res/
│   │   │   ├── layout/              # Layouts XML
│   │   │   └── values/              # Strings, cores, temas
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
└── README.md (este arquivo)
```

## 🚀 Início Rápido

1. **Hospede seu Streamlit** (veja `QUICK_START_ANDROID.md`)
2. **Configure a URL** em `MainActivity.java` (linha ~20)
3. **Abra no Android Studio**
4. **Execute** ▶️

Para instruções detalhadas, veja:
- `QUICK_START_ANDROID.md` - Guia rápido
- `COMO_TESTAR.md` - **Como testar o app** 🧪
- `README_ANDROID.md` - Documentação completa
- `CONFIG.md` - Opções de configuração

## 📋 Requisitos

- Android Studio (última versão)
- Android SDK (API 24+)
- App Streamlit hospedado (Streamlit Cloud ou servidor próprio)

## 🔗 Links Úteis

- [Android Studio Download](https://developer.android.com/studio)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Documentação Android](https://developer.android.com/docs)

## 📝 Notas

- O app usa WebView para carregar o Streamlit
- Funciona offline apenas se o Streamlit estiver em cache
- Para produção, use HTTPS e remova `usesCleartextTraffic`

## 🤝 Suporte

Consulte os arquivos de documentação:
- `README_ANDROID.md` - Guia completo
- `QUICK_START_ANDROID.md` - Início rápido
- `CONFIG.md` - Configurações avançadas


