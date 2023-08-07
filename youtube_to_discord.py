import discord
from discord.ext import commands
from dotenv import dotenv_values
import yt_dlp

API_KEYS = dotenv_values(".env")

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
    
queue = []

def check_queue(ctx):
    if len(queue) > 0:
        url = queue.pop(0)
        play_song(ctx, url)

def play_song(ctx, url):
    voice_client = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp',  # Nom du fichier temporaire
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio('temp.mp3'), after=lambda e: check_queue(ctx))  # Joue le fichier téléchargé

    
@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client

    if voice_client is None:
        await ctx.send("Je ne suis pas dans un canal vocal.")
        return

    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Musique arrêtée.")
    else:
        await ctx.send("Aucune musique en cours de lecture.")

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
        queue.append(url)
        await ctx.send(f'Chanson ajoutée à la file d\'attente.')
    else:
        await ctx.send(f'Joue la chanson...')
        play_song(ctx, url)

@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client

    if voice_client is None:
        await ctx.send("Je ne suis pas dans un canal vocal.")
        return

    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Chanson passée.")
    else:
        await ctx.send("Aucune musique en cours de lecture pour sauter.")

bot.run(TOKEN)