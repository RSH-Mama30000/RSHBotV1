import discord
import platform
import yt_dlp
import random
import os

from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
last_audoi_url = None
last_audoi_title = None

load_dotenv(r"Bot Discord/RSHBot/tokv1.env")
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

class Commandes(commands.Cog):
    def init(self, bot):
        self.bot = bot

@bot.tree.command(name="commande", description="Affiche toutes les commandes disponibles.")
async def commande(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 Liste des commandes", color=discord.Color.purple())

    for category, cmds in categories.items():
        embed.add_field(name=f"📂 {category}", value="\u200b", inline=False)
        for cmd_name, cmd_info in cmds.items():
            embed.add_field(
                name=f"🔹 {cmd_name}",
                value=f"{cmd_info['description']} *(Syntaxe : `{cmd_info['syntax']}`)*",
                inline=False
            )

    await interaction.response.send_message(embed=embed)

categories = {
        "Musique": {
            "Jouer": {"description": "Joue de la musique dans un salon vocal.", "syntax": "!jouer [URL]"},
            "Arrêter": {"description": "Arrête la musique en cours.", "syntax": "!arrêté"},
            "Rejoindre": {"description": "Fait rejoindre le bot dans un salon vocal.", "syntax": "!rejoindre"},
            "Quitter": {"description": "Quitte le salon vocal.", "syntax": "!quitter"},
        },
        "Jeux & Fun": {       
            "Boite Mystere": {"description": "Ouvre une boîte mystère pour découvrir une récompense aléatoire.", "syntax": "!boitemystere"},
            "Pile ou Face": {"description": "Lance une pièce pour jouer à Pile ou Face.", "syntax": "!pileouface"},
            "EightBall": {"description": "Pose une question et reçois une réponse aléatoire.", "syntax": "!eightball"},
        },
        "Utilitaires": {
            "Bot Info": {"description": "Affiche des informations sur le bot.", "syntax": "!botinfo"},
            "Dire": {"description": "Fait dire quelque chose au bot.", "syntax": "!dire [message]"},
            "Effacer": {"description": "Efface un certain nombre de messages.", "syntax": "!effacer [nombre]"},
            "Avatar": {"description": "Affiche la photo de profil d'un utilisateur.", "syntax": "!avatar [ID discord]"},
            "Latence": {"description": "Voir la latence du bot.", "syntax": "!latence"},
        },
        "Discussion": {
            "Bonjour": {"description": "Envoyer des salutations.", "syntax": "!bonjour"},
            "Morton": {"description": "Morton On Top.", "syntax": "!morton"},
            "El Pepe": {"description": "Informations sur El Pepe.", "syntax": "!elpepe"},
        }
    }

activities = [
    discord.Game("Morton On Top"),
    discord.Game("/commande pour voir ce que je sais faire"),
    discord.Game("Python 3.11"),
    discord.Game("Crée par mama30000"),
    discord.Game('https://discord.gg/nAZGdXMcmM')
]

@tasks.loop(seconds=10)
async def change_activity():
    
    activity = random.choice(activities)
    await bot.change_presence(activity=activity)    

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()
    print("🤖 Commandes slash synchronisées.")
    change_activity.start()

@bot.command(help="Salutations!")
async def bonjour(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention}!")
        
@bot.command(help="Envoyer un message sous l'identité de RSHBot.")
async def dire(ctx, *, message):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.send(f"{message}")
    else:
        await ctx.send("Désolé vous n'avez pas les permissions pour utiliser cette commande")
        return
    await ctx.message.delete()
    
@bot.command(name="botinfo", help="Affiche des informations sur le bot.")
async def botinfo(ctx):
    bot_user = bot.user
    python_version = platform.python_version()
    discord_version = discord.__version__ 
    guild_count = len(bot.guilds)
    member_count = sum(g.member_count for g in bot.guilds)

    embed = discord.Embed(
        title="🤖 Informations du Bot",
        description="Voici quelques détails sur moi !",
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url=bot_user.avatar.url if bot_user.avatar else bot_user.default_avatar.url)
    embed.add_field(name="📛 Nom du bot", value=bot_user.name, inline=True)
    embed.add_field(name="🔢 ID", value=bot_user.id, inline=True)
    embed.add_field(name="📅 Créé le", value=bot_user.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🌎 Serveurs", value=f"{guild_count} serveurs", inline=True)
    embed.add_field(name="👥 Membres total", value=f"{member_count} membres", inline=True)
    embed.add_field(name="🐍 Version Python", value=python_version, inline=True)
    embed.add_field(name="⚙️ Version discord.py", value=discord_version, inline=True)

    embed.set_footer(text=f"Commandé par {ctx.author.name}", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed)
    
@bot.command(name='rejoindre',help='Rejoindre le salon vocal')
async def rejoindre(ctx):
   if ctx.author.voice:
       channel = ctx.author.voice.channel
       await channel.connect()
       await ctx.send(f'Je rejoins le salon vocal : **{channel.name}**')
   else:
    await ctx.send("Tu dois être dans un salon vocal pour que je puisse te rejoindre")    
    
@bot.command(name='quitter', help='Quitte le salon vocal.')
async def quitter(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Je quitte le salon vocal.")
    else:
        await ctx.send("Je ne suis pas dans un salon vocal.")
        
@bot.command(name='jouer', help='Jouer de la musique')
async def jouer(ctx, url: str):
    if ctx.author.voice is None:
        await ctx.send("Tu dois être dans un canal vocal pour utiliser cette commande.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        voice_client = await channel.connect()
        await ctx.send(f"Je t'ai rejoint dans **{channel}** !")
    else:
        voice_client = ctx.voice_client
        await voice_client.move_to(channel)
        await ctx.send(f"Je me suis déplacé dans **{channel}** !")

    if voice_client.is_playing():
        voice_client.stop()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Musique inconnue')

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    voice_client.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
    await ctx.send(f"🎵 Lecture de **{title}**")
    
    global last_audio_url, last_audio_title
    last_audio_url = audio_url
    last_audio_title = title
    
@bot.command(name='volume', help='Changer le volume de la musique actuelle (0 à 100)')
async def volume(ctx, pourcentage: int):
    global last_audio_url, last_audio_title

    if pourcentage < 0 or pourcentage > 100:
        await ctx.send("Le volume doit être entre 0 et 100.")
        return

    voice_client = ctx.voice_client
    if voice_client is None or not voice_client.is_connected():
        await ctx.send("Je ne suis connecté à aucun salon vocal.")
        return

    if last_audio_url is None:
        await ctx.send("Aucune musique récente à rejouer.")
        return

    if voice_client.is_playing():
        voice_client.stop()

    import math
    gain_db = 20 * math.log10(pourcentage / 100) if pourcentage > 0 else -100

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': f'-vn -af "volume={gain_db}dB"'
    }

    voice_client.play(discord.FFmpegPCMAudio(last_audio_url, **FFMPEG_OPTIONS))
    await ctx.send(f"🔊 Volume ajusté à **{pourcentage}%** pour **{last_audio_title}**.")

@bot.command(name='arrêté', help='Arrêté la musique')
async def arrêté(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Musique arrêtée.")
    else:
        await ctx.send("Aucune musique n'est en cours de lecture.")    

rewards = [
    {"nom": "💰 100 pièces d'or", "effet": "Tu deviens plus riche !"},
    {"nom": "🎟️ Ticket VIP", "effet": "Tu es maintenant un membre d'honneur !"},
    {"nom": "🍀 Trèfle à 4 feuilles", "effet": "La chance est de ton côté !"},
    {"nom": "💎 Diamant rare", "effet": "Tu es maintenant un vrai boss !"},
    {"nom": "👻 Fantôme effrayant", "effet": "Boo ! Il te suit partout maintenant..."},
    {"nom": "🔥 Feu magique", "effet": "Attention, ça brûle !"},
    {"nom": "💩 Tas de caca", "effet": "Oh non... Ça sent mauvais !"},
]

@bot.command(name="boitemystere", help="Ouvrir une boîte mystère et découvrir une récompense aléatoire.")
async def boitemystere(ctx):
    reward = random.choice(rewards)

    embed = discord.Embed(
        title="🎁 Boîte Mystère Ouverte !",
        description=f"Tu as gagné : **{reward['nom']}**\n\n_{reward['effet']}_",
        color=discord.Color.gold()
    )

    await ctx.send(embed=embed)
    
@bot.command(help="Efface les messages.")
async def effacer(ctx, amount : int):
    if amount <= 0 or amount > 500:
        return await ctx.send("Veuillez entrer un nombre entre **1 et 500**.")

    deleted_messages = await ctx.channel.purge(limit=amount) 
    await ctx.send(f"J'ai effacé {len(deleted_messages)} messages.")
    
@bot.command(help="Permet de voir latence du bot.")
async def latence(ctx):
    await ctx.send(f"La latence du bot est de {round(bot.latency * 1000)}")
    await ctx.message.delete()           
    
@bot.command(help="Répond à une question  par une réponse aléatoire !")
async def eightball(ctx):
    responses = [
        "Oui !", "Non", "Peut-être...", "Je ne sais pas", "Bien sur", "Je ne pense pas...", "Absolument !", "Jamais !"
    ]
    await ctx.send(random.choice(responses))    
    
@bot.command(help="Voir la photo de profil d'un utilisateur")
async def avatar(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    if user:
        embed = discord.Embed(title=f"Avatar de {user.name}", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Utilisateur non trouvé.")    
        
@bot.command(help="Morton On Top")
async def morton(ctx):
    await ctx.send(f"Morton On Top, Mancini On Flop")
    
@bot.command(help="Description de El Pepe")
async def elpepe(ctx):
    await ctx.send(f"El Pepe aussi connu sous le nom de Jonathan Suzanne est une grosse pute de merde et je baise sa salope de mère.")            

bot.run(TOKEN)
