import discord
from discord.ext import commands
from dotenv import dotenv_values
import yt_dlp

API_KEYS = dotenv_values(".env")

TOKEN = API_KEYS["API_KEY_DISCORD2"]

intents = discord.Intents.default()
intents.members = True
# bot = commands.Bot(command_prefix='>',intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)

loop = False
queue = []

async def send_control_buttons(ctx):
    control_message = await ctx.send("Cliquez sur les réactions pour contrôler la lecture!")
    reactions = ["⏯", "⏭", "🔁"]  # Play/Pause, Skip, Loop
    for reaction in reactions:
        await control_message.add_reaction(reaction)
    return control_message

def check_queue(ctx):
    if len(queue) > 0:
        next_url = queue.pop(0)
        play_song(ctx, next_url)

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
        voice_client.play(discord.FFmpegPCMAudio('temp.mp3'), after=lambda e: check_queue(ctx))
        voice_client.source = discord.FFmpegPCMAudio('temp.mp3')

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté!')

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
async def p(ctx, url):
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
        await send_control_buttons(ctx)

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

@bot.command()
async def loop(ctx):
    global loop
    loop = not loop

    if loop:
        await ctx.send("Boucle activée.")
    else:
        await ctx.send("Boucle désactivée.")
        
@bot.command()
async def h(ctx):
    embed = discord.Embed(title="Aide pour le Bot", description="Voici les commandes que vous pouvez utiliser:", color=0x00ff00)
    
    embed.add_field(name="`join`", value="Rejoindre le canal vocal de l'utilisateur.", inline=False)
    embed.add_field(name="`leave`", value="Quitter le canal vocal actuel.", inline=False)
    embed.add_field(name="`p <URL>`", value="Jouer une chanson à partir d'un lien YouTube.", inline=False)
    embed.add_field(name="`skip`", value="Passer à la chanson suivante dans la file d'attente.", inline=False)
    embed.add_field(name="`stop`", value="Arrêter la musique en cours.", inline=False)
    embed.add_field(name="`loop`", value="Activer/désactiver la boucle de la chanson actuelle.", inline=False)
    embed.add_field(name="`ping`", value="Tester la latence du bot.", inline=False)
    
    await ctx.send(embed=embed)


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    ctx = await bot.get_context(reaction.message)

    if reaction.emoji == "⏯":
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            ctx.voice_client.resume()

    elif reaction.emoji == "⏭":
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    elif reaction.emoji == "🔁":
        global loop
        loop = not loop

    await reaction.message.remove_reaction(reaction.emoji, user)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Une erreur est survenue: {error}')

bot.run(TOKEN)

#Modifie maintenant le script pour que les commandes fonctionnent avec le point d'exclamation, il n'y a plus besoin de taper le nom du bot.