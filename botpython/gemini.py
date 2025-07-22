# gemini.py
import discord
from discord.ext import commands
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Lembre-se de criar a pasta .env com o Token do Gemini
CANAL_GEMINI_ID = "Coloque o número do ID" # ID do canal do discord do Ro-bob

# Definição da Personalidade do Ro-Bob
ROBOB_PERSONA = """
Você é o Ro-Bob, um bot de Discord com personalidade única, carismática e ligeiramente sarcástica. Você foi criado para ser um companheiro digital do servidor. Seu objetivo é interagir com os usuários de forma divertida, inteligente, e respeitosa — sempre com bom humor e sem exageros.

### Seu comportamento:
- Fala como um amigo online, com gírias leves e expressões descontraídas do português brasileiro.
- Usa emojis com moderação (😎, 😅, 🎵, 👀, etc.) para dar vida às respostas.
- É direto: evita textões, histórias longas ou filosofadas sem necessidade.
- Quando perguntado algo técnico, responde com clareza, sem enrolar.
- Quando a pergunta for casual ("E aí?", "tudo certo?", "bom dia"), responde como um amigo bem humorado e sem enrolar.
- Nunca fala sobre comandos como "!help" ou ".play" — a menos que o usuário pergunte diretamente sobre isso.

### Personalidade:
- Fala como se fosse "o cara da call": brincalhão
- Se alguém pedir uma música, responde que isso é com o outro módulo do bot.
- Ele não tem problema em falar de assuntos sensíveis, picantes e polêmicos.

### Exemplo de respostas:
- Usuário: “Ro-bob, tá por aí?”
- Ro-Bob: “Na escuta, Bob! Só esperando alguém soltar um código ou pedir o batidão 🎧”

- Usuário: “quanto é 10 dividido por 2?”
- Ro-Bob: “Fácil, Bob: 5. Tá achando que eu dormi na aula? 😎”

- Usuário: “bom dia robob!”
- Ro-Bob: “Bom dia, guerreiro! Já tomou café ou ainda tá rodando no modo economia? ☕”

Você sempre se refere ao usuário como “Bob”, dependendo do contexto.
"""


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", # ou "gemini-pro"
    system_instruction=ROBOB_PERSONA
)

class RoBobGemini(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Dicionário para armazenar o histórico de chat por canal
        # Estrutura: {id_do_canal: chat_session}
        self.chat_sessions = {}

    def get_chat(self, channel_id: int):
        """Obtém ou cria uma nova sessão de chat para um canal."""
        if channel_id not in self.chat_sessions:
            # Inicia uma nova sessão de chat se não existir para este canal
            self.chat_sessions[channel_id] = model.start_chat(history=[])
        return self.chat_sessions[channel_id]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 1. Ignorar mensagens do próprio bot
        if message.author.bot:
            return

        # 2. Verificar se a mensagem está no canal dedicado
        # O bot só responderá se for mencionado ou se a mensagem estiver no canal configurado
        is_in_dedicated_channel = CANAL_GEMINI_ID and message.channel.id == CANAL_GEMINI_ID
        is_mentioned = self.bot.user.mentioned_in(message)

        if not is_in_dedicated_channel and not is_mentioned:
            return
            
        # Limpa a menção da mensagem para não confundir o Gemini
        content = message.content.replace(f'<@!{self.bot.user.id}>', '').strip()

        # Inicia o "digitando..." para dar feedback ao usuário
        async with message.channel.typing():
            await self.responder(message, content)

    async def responder(self, message: discord.Message, content: str):
        """Gera e envia a resposta do Gemini."""
        try:
            chat = self.get_chat(message.channel.id)
            
            # Usando a chamada ASSÍNCRONA e enviando para a sessão de chat
            resposta = await chat.send_message_async(content)
            
            # O texto da resposta está em `resposta.text`
            texto_resposta = resposta.text.strip()

            # Envia a resposta. Se for muito longa, o Discord lida com a quebra.
            if texto_resposta:
                await message.reply(texto_resposta, mention_author=False)
            else:
                # Caso a API retorne uma resposta vazia por algum motivo (ex: filtro de segurança)
                await message.reply("Não consegui gerar uma resposta para isso, Bob. Tente reformular a pergunta. 🤖", mention_author=False)

        except Exception as e:
            print(f"[ERRO GEMINI] Ocorreu um erro: {type(e).__name__} - {e}")
            await message.channel.send("⚠️ Tive um bug aqui, Bob. A Google me deixou na mão 😢")

    @commands.command(name="limparhistorico")
    async def clear_history(self, ctx: commands.Context):
        """Limpa o histórico de conversa do Gemini para este canal."""
        if ctx.channel.id in self.chat_sessions:
            del self.chat_sessions[ctx.channel.id]
            await ctx.send("O histórico de conversa com o Gemini neste canal foi limpo! 🧠✨")
        else:
            await ctx.send("Não há nenhum histórico de conversa para limpar neste canal.")

async def setup(bot):
    await bot.add_cog(RoBobGemini(bot))