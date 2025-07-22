# musica.py
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
from collections import deque

# Criação da fila de música
FILA_MUSICA = {}

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Comando de /play
    @app_commands.command(name="play", description="Tocar a música.")
    @app_commands.describe(song_query="Search query")
    async def play(self, interaction: discord.Interaction, song_query: str):
        await interaction.response.defer()

        voice_channel = interaction.user.voice.channel

        if voice_channel is None:
            await interaction.followup.send("Fala, Bob. Entre em um canal de voz e mande novamente o comando.")
            return

        voice_client = interaction.guild.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)

        ydl_options = {
            "format": "bestaudio[abr<=96]/bestaudio",
            "noplaylist": True,
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
        }

        results = await self.search_ytdlp_async("ytsearch1:" + song_query, ydl_options)
        tracks = results.get("entries", [])

        if not tracks:
            await interaction.followup.send("Não encontrei essa música.")
            return

        audio_url = tracks[0]["url"]
        title = tracks[0].get("title", "Sem título")

        guild_id = str(interaction.guild_id)
        if FILA_MUSICA.get(guild_id) is None:
            FILA_MUSICA[guild_id] = deque()

        FILA_MUSICA[guild_id].append((audio_url, title))

        if voice_client.is_playing() or voice_client.is_paused():
            await interaction.followup.send(f"Boa escolha! Adicionado à fila: **{title}**")
        else:
            await interaction.followup.send(f"Tocando agora: **{title}**")
            await self.play_next_song(voice_client, guild_id, interaction.channel)

# Comando de /pause
    @app_commands.command(name="pause", description="Pause a música atual.")
    async def pause(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            return await interaction.response.send_message("Bob nem tá na call.")

        if not voice_client.is_playing():
            return await interaction.response.send_message("Não tem nada tocando.")
        
        voice_client.pause()
        await interaction.response.send_message("Pausando...")

# Comando de /resume
    @app_commands.command(name="resume", description="Despausa a música pausada.")
    async def resume(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            return await interaction.response.send_message("Bob não está conectado.")

        if not voice_client.is_paused():
            return await interaction.response.send_message("Nada está pausado.")

        voice_client.resume()
        await interaction.response.send_message("Voltando com o batidão!")
        
# Comando de /stop
    @app_commands.command(name="stop", description="Parar e sair do canal de voz.")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send("Bob, não estou conectado.")
        
        guild_id = str(interaction.guild_id)
        if guild_id in FILA_MUSICA:
            FILA_MUSICA[guild_id].clear()
            
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
                
            await voice_client.disconnect()
            await interaction.response.send_message("Parando e vazando. Falou, Bob!")

# Comando de /pular
    @app_commands.command(name="pular", description="Pular a música atual.")
    async def pular(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()
            await interaction.response.send_message("Pulando...")
        else:
            await interaction.response.send_message("Nada na fila, Bob.")

    async def play_next_song(self, voice_client, guild_id, channel):
        if FILA_MUSICA[guild_id]:
            audio_url, title = FILA_MUSICA[guild_id].popleft()

            ffmpeg_options = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn -c:a libopus -b:a 96k",
            }

            source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options)

            def after_play(error):
                if error:
                    print(f"Erro: {error}")
                asyncio.run_coroutine_threadsafe(
                    self.play_next_song(voice_client, guild_id, channel), self.bot.loop
                )

            voice_client.play(source, after=after_play)
            await channel.send(f"Tocando agora: **{title}**")
        else:
            await voice_client.disconnect()
            FILA_MUSICA[guild_id] = deque()

    async def search_ytdlp_async(self, query, ydl_opts):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self._extract(query, ydl_opts))

    def _extract(self, query, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(query, download=False)

async def setup(bot):
    await bot.add_cog(Musica(bot))