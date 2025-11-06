# 🧪 Como Testar o App Android

Este guia mostra como testar o app em diferentes cenários.

## 📋 Índice

1. [Testar Streamlit Localmente](#1-testar-streamlit-localmente)
2. [Testar no Emulador Android](#2-testar-no-emulador-android)
3. [Testar no Dispositivo Físico](#3-testar-no-dispositivo-físico)
4. [Testar com Streamlit Cloud](#4-testar-com-streamlit-cloud)
5. [Solução de Problemas](#solução-de-problemas)

---

## 1. Testar Streamlit Localmente

Antes de testar o app Android, certifique-se de que o Streamlit funciona no navegador.

### Passo 1: Iniciar o Streamlit

```bash
# No diretório do projeto
streamlit run streamlit_app.py
```

Você verá algo como:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.X:8501
```

### Passo 2: Testar no Navegador

1. Abra `http://localhost:8501` no navegador
2. Verifique se o app carrega corretamente
3. Teste as funcionalidades (selecionar ligas, ver dados, etc.)

✅ **Se funcionar no navegador, está pronto para testar no Android!**

---

## 2. Testar no Emulador Android

### Passo 1: Criar um Emulador

1. Abra o **Android Studio**
2. Vá em `Tools > Device Manager` (ou ícone de dispositivo na barra)
3. Clique em `Create Device`
4. Escolha um dispositivo (ex: Pixel 5)
5. Escolha uma imagem do sistema (ex: Android 13 - API 33)
6. Clique em `Finish`

### Passo 2: Iniciar o Emulador

1. No Device Manager, clique no ▶️ ao lado do dispositivo criado
2. Aguarde o emulador iniciar (pode demorar alguns minutos na primeira vez)

### Passo 3: Configurar URL no App

Edite `MainActivity.java`:

```java
// Para emulador, use 10.0.2.2 (não localhost!)
private static final String STREAMLIT_URL = "http://10.0.2.2:8501";
```

**Importante:** `10.0.2.2` é o endereço especial do Android Emulator que aponta para `localhost` do seu computador.

### Passo 4: Iniciar o Streamlit

Em um terminal, inicie o Streamlit:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

O `--server.address 0.0.0.0` permite conexões externas.

### Passo 5: Executar o App

1. No Android Studio, certifique-se de que o emulador está selecionado
2. Clique em ▶️ **Run** ou pressione `Shift+F10`
3. Aguarde o app instalar e abrir
4. O app deve carregar o Streamlit automaticamente

### ✅ Verificar se Funcionou

- O app abre sem erros
- A barra de progresso aparece e some
- O conteúdo do Streamlit é exibido
- Você consegue interagir com o dashboard

---

## 3. Testar no Dispositivo Físico

### Passo 1: Preparar o Dispositivo

1. **Ativar Modo Desenvolvedor:**
   - Vá em `Configurações > Sobre o telefone`
   - Toque 7 vezes em "Número da versão" ou "Build number"
   - Você verá "Você agora é um desenvolvedor!"

2. **Ativar Depuração USB:**
   - Vá em `Configurações > Opções do desenvolvedor`
   - Ative "Depuração USB"

3. **Conectar ao Computador:**
   - Conecte o dispositivo via USB
   - No dispositivo, aparecerá um aviso: "Permitir depuração USB?"
   - Marque "Sempre permitir deste computador" e toque em "OK"

### Passo 2: Descobrir o IP do Computador

**Windows:**
```powershell
ipconfig
```
Procure por "Endereço IPv4" (ex: `192.168.1.100`)

**Linux/Mac:**
```bash
ifconfig
# ou
ip addr show
```

### Passo 3: Configurar URL no App

Edite `MainActivity.java`:

```java
// Use o IP do seu computador (mesma rede Wi-Fi)
private static final String STREAMLIT_URL = "http://192.168.1.100:8501";
```

**Substitua `192.168.1.100` pelo IP do seu computador!**

### Passo 4: Iniciar o Streamlit

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### Passo 5: Conectar Dispositivo e Executar

1. No Android Studio, você verá o dispositivo na lista
2. Selecione o dispositivo físico
3. Clique em ▶️ **Run**
4. O app será instalado e executado no dispositivo

### ⚠️ Importante: Mesma Rede Wi-Fi

- Computador e dispositivo devem estar na **mesma rede Wi-Fi**
- Firewall do Windows pode bloquear - permita o Streamlit

**Permitir no Firewall do Windows:**
1. `Configurações > Firewall do Windows Defender`
2. `Permitir um aplicativo pelo Firewall`
3. Adicione Python ou permita porta 8501

---

## 4. Testar com Streamlit Cloud

### Passo 1: Fazer Deploy no Streamlit Cloud

1. Acesse https://streamlit.io/cloud
2. Conecte seu GitHub
3. Selecione o repositório
4. Configure:
   - **Main file:** `streamlit_app.py`
   - **Secrets:** Adicione `FOOTBALL_DATA_API_KEY`
5. Aguarde o deploy (URL: `https://seu-app.streamlit.app`)

### Passo 2: Configurar URL no App

Edite `MainActivity.java`:

```java
private static final String STREAMLIT_URL = "https://seu-app.streamlit.app";
```

### Passo 3: Remover Permissão HTTP (Opcional)

Para produção, remova HTTP não criptografado do `AndroidManifest.xml`:

```xml
<!-- Remova esta linha para produção -->
<!-- android:usesCleartextTraffic="true" -->
```

### Passo 4: Testar

1. Execute o app no dispositivo ou emulador
2. O app deve carregar o Streamlit Cloud
3. Funciona de qualquer lugar (não precisa estar na mesma rede)

---

## 🔍 Verificar Logs e Debug

### Android Studio Logcat

1. Abra o **Logcat** no Android Studio (aba inferior)
2. Filtre por `MainActivity` ou `WebView`
3. Procure por erros em vermelho

### Verificar Erros Comuns

**Erro: "net::ERR_CONNECTION_REFUSED"**
- Streamlit não está rodando
- URL incorreta
- Firewall bloqueando

**Erro: "net::ERR_CLEARTEXT_NOT_PERMITTED"**
- Tentando usar HTTP em Android 9+
- Adicione `usesCleartextTraffic="true"` no AndroidManifest
- Ou use HTTPS

**App abre mas fica em branco:**
- Verifique se o JavaScript está habilitado
- Verifique logs no Logcat
- Teste a URL no navegador do dispositivo primeiro

### Testar URL no Navegador do Dispositivo

1. Abra o Chrome no dispositivo/emulador
2. Digite a URL do Streamlit
3. Se funcionar no navegador, deve funcionar no app

---

## 🧪 Checklist de Testes

### Funcionalidades Básicas
- [ ] App abre sem erros
- [ ] WebView carrega o Streamlit
- [ ] Barra de progresso funciona
- [ ] Conteúdo é exibido corretamente

### Interações
- [ ] Botão voltar funciona (volta na navegação do WebView)
- [ ] É possível interagir com o dashboard
- [ ] Seleção de ligas funciona
- [ ] Dados são carregados

### Diferentes Cenários
- [ ] Testado no emulador
- [ ] Testado no dispositivo físico
- [ ] Testado com Streamlit local
- [ ] Testado com Streamlit Cloud

### Performance
- [ ] App carrega em tempo razoável
- [ ] Não trava durante o uso
- [ ] Memória não aumenta excessivamente

---

## 🐛 Solução de Problemas

### Problema: App não carrega

**Solução 1: Verificar Streamlit**
```bash
# Verifique se está rodando
streamlit run streamlit_app.py
```

**Solução 2: Verificar URL**
- Emulador: `http://10.0.2.2:8501`
- Dispositivo: `http://IP_DO_COMPUTADOR:8501`
- Cloud: `https://seu-app.streamlit.app`

**Solução 3: Verificar Permissões**
- Internet está habilitada no dispositivo?
- Firewall está bloqueando?

### Problema: Erro de conexão no dispositivo físico

**Solução:**
1. Verifique se estão na mesma rede Wi-Fi
2. Desative temporariamente o firewall
3. Use o IP correto do computador
4. Teste a URL no navegador do dispositivo primeiro

### Problema: App trava ou fecha

**Solução:**
1. Verifique os logs no Logcat
2. Verifique se há erros de memória
3. Teste em um dispositivo mais recente
4. Verifique se o Streamlit não está sobrecarregado

### Problema: Conteúdo não aparece

**Solução:**
1. Verifique se JavaScript está habilitado no WebView
2. Verifique se o Streamlit carrega no navegador
3. Limpe o cache do WebView (adicione no código se necessário)
4. Verifique CORS no servidor Streamlit

---

## 📱 Testar APK Gerado

### Gerar APK de Debug

```bash
cd android-app
./gradlew assembleDebug
```

### Instalar no Dispositivo

**Via USB (ADB):**
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

**Via Arquivo:**
1. Copie o APK para o dispositivo
2. Abra o arquivo no dispositivo
3. Permita instalação de fontes desconhecidas
4. Instale o app

### Testar APK Instalado

1. Abra o app no dispositivo
2. Verifique se funciona como esperado
3. Teste todas as funcionalidades

---

## ✅ Pronto para Produção?

Antes de publicar:

- [ ] Testado em diferentes dispositivos
- [ ] Testado em diferentes versões do Android
- [ ] URL configurada para produção (HTTPS)
- [ ] `usesCleartextTraffic` removido (se usando HTTPS)
- [ ] APK assinado gerado
- [ ] Ícone e nome do app personalizados
- [ ] Versão atualizada no `build.gradle`

---

## 📞 Precisa de Ajuda?

1. Verifique os logs no **Logcat**
2. Teste a URL no navegador do dispositivo
3. Verifique se o Streamlit funciona no navegador do PC
4. Consulte `README_ANDROID.md` para mais detalhes

