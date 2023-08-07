import discord
from discord.ext import commands
from dotenv import dotenv_values
import openai
import yt_dlp

API_KEYS = dotenv_values(".env")

openai.api_key = API_KEYS["API_KEY_OPENAI"]
TOKEN = API_KEYS["API_KEY_DISCORD2"]

intents = discord.Intents.default()
intents.members = True
# bot = commands.Bot(command_prefix='>',intents=intents)

def get_prefix(bot, message):
    return commands.when_mentioned(bot, message)

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté!')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Une erreur est survenue: {error}')

@bot.command()
async def test(ctx):
    await ctx.send('Test réussi!')

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Vous devez être dans un canal vocal.")
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"Connecté à {channel}")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("Je ne suis pas dans un canal vocal.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("Déconnecté du canal vocal.")


@bot.command()
async def play(ctx, url):
    voice_client = ctx.voice_client

    if voice_client is None:
        await ctx.send("Je dois être dans un canal vocal pour jouer l'audio.")
        return

    if voice_client.is_playing():
        voice_client.stop()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp', # Nom du fichier temporaire
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio('temp.mp3')) # Joue le fichier téléchargé

bot.run(TOKEN)