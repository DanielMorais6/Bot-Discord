# main.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Carrega todas as variáveis de ID com segurança
# Lembre-se de criar a pasta .env com os Tokens do Discord e Gemini 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()


class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        # Carrega os módulos (extensões/Cogs)
        await self.load_extension("musica")
        await self.load_extension("gemini")
        await self.tree.sync()
        print("Comandos sincronizados com o Discord.")

bot = MeuBot()

@bot.event
async def on_ready():
    print(f"{bot.user} está online e pronto para ser usado!")

bot.run(TOKEN)