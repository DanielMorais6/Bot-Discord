# 🤖 Ro-Bob — Bot do Discord com Música + IA (Gemini)

O **Ro-Bob** é um bot multifuncional para servidores Discord, desenvolvido por mim, Daniel, como parte do meu aprendizado em programação e desenvolvimento de bots. Ele é um companheiro digital que toca música, conversa com os membros usando inteligência artificial e deixa o servidor muito mais interativo.

> **Tecnologias utilizadas:**  
> `Python`, `discord.py`, `yt-dlp`, `FFmpeg`, `Gemini API`, `asyncio`, `dotenv`

---

## 📌 Funcionalidades

### 🎵 Comandos de Música (YouTube)
- `/play [nome da música]` → pesquisa e toca músicas diretamente do YouTube
- `/pause` → pausa a música atual
- `/resume` → continua a reprodução
- `/pular` → pula para a próxima
- `/parar` → para e desconecta do canal de voz
- 🎶 Suporte a fila por servidor, tocando músicas em sequência

### 💬 Chat com Inteligência Artificial (Gemini)
- O canal designado permite **conversar diretamente com o Ro-Bob**, alimentado pelo **Gemini**
- O bot responde de forma contextual e divertida, como um verdadeiro companheiro do servidor

---

## 🛠️ Pré-requisitos

- Python 3.10 ou superior
- Token do bot do Discord
- API Key da Gemini
- FFmpeg instalado e adicionado ao PATH
- Ambiente `.env` configurado com suas chaves

---

## ⚙️ Como rodar localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/ro-bob.git
   cd ro-bob

2. **Clone o arquivo .env**
    DISCORD_TOKEN=seu_token_aqui
    OPENAI_API_KEY=sua_chave_openai_aqui

3. **Instale as dependências**
    pip install -r requirements.txt

4. **Rode o Bot**
    python main.py

# 📁 Estrutura do Projeto

    ro-bob/
    ├── main.py                # Arquivo principal
    ├── musica.py              # Módulo com os comandos de música
    ├── gemini.py              # módulo com integração à IA
    ├── .env                   # Chaves privadas (NÃO subir no GitHub)
    ├── requirements.txt
    └── README.md

# 💡 Possíveis melhorias futuras
    
    🎤 Comando de letras de músicas
    🔒 Comandos exclusivos para administradores
    🌐 Dashboard web com Flask ou FastAPI
    ☁️ Hospedagem 24/7 (Replit / VPS / Railway)

# 📄 Licença
    Este projeto é de código aberto sob a licença MIT. Sinta-se à vontade para usar, melhorar e contribuir!