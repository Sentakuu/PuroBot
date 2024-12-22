import discord
from discord.ext import commands
import os
import random
import base64
import names
import string
import secrets
import json
import requests
import datetime

# Get environment variables (from Railway)
TOKEN = os.getenv('DISCORD_TOKEN')
FORTNITE_API_KEY = os.getenv('FORTNITE_API_KEY')
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='p!', intents=intents)

# Constants
OWNER_ROLE_NAME = "Puro"
TRANSFUR_RESPONSES = [
    "*Puro sneaks up behind you and hugs you tight, covering you in black latex*",
    "*The black goo slowly envelops you, transforming you into a cute latex creature*",
    "*You feel the warm embrace of the dark latex, becoming one with Puro*",
    "*The transformation begins, your form shifting into a latex being*"
]

MINECRAFT_COLORS = {
    "§0": "Black",
    "§1": "Dark Blue",
    "§2": "Dark Green",
    "§3": "Dark Aqua",
    "§4": "Dark Red",
    "§5": "Dark Purple",
    "§6": "Gold",
    "§7": "Gray",
    "§8": "Dark Gray",
    "§9": "Blue",
    "§a": "Green",
    "§b": "Aqua",
    "§c": "Red",
    "§d": "Light Purple",
    "§e": "Yellow",
    "§f": "White",
    "§k": "Obfuscated",
    "§l": "Bold",
    "§m": "Strikethrough",
    "§n": "Underline",
    "§o": "Italic",
    "§r": "Reset"
}

@bot.event
async def on_ready():
    print(f'🐺 {bot.user} is ready to spread some latex love!')
    await bot.change_presence(activity=discord.Game(name="Changed | p!help"))

@bot.command(name='transfur')
async def transfur(ctx):
    if discord.utils.get(ctx.author.roles, name=OWNER_ROLE_NAME):
        response = random.choice(TRANSFUR_RESPONSES)
        await ctx.send(response)
    else:
        await ctx.send("*Puro looks at you confused* Only my special friend can use this command!")

@bot.command(name='fortnite')
async def fortnite_stats(ctx, username: str):
    if not FORTNITE_API_KEY:
        await ctx.send("*Puro is sad* Fortnite API key is not configured!")
        return

    headers = {'Authorization': FORTNITE_API_KEY}
    url = f'https://fortnite-api.com/v2/stats/br/v2?name={username}'
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            stats = data['data']['stats']['all']['overall']
            embed = discord.Embed(title=f"Fortnite Stats for {username}", color=0x000000)
            embed.add_field(name="Wins", value=stats['wins'], inline=True)
            embed.add_field(name="Matches", value=stats['matches'], inline=True)
            embed.add_field(name="Win Rate", value=f"{stats['winRate']}%", inline=True)
            embed.add_field(name="Kills", value=stats['kills'], inline=True)
            embed.add_field(name="K/D Ratio", value=stats['kd'], inline=True)
            embed.set_footer(text="*Puro loves tracking stats! 📊*")
            await ctx.send(embed=embed)
        else:
            await ctx.send("*Puro couldn't find that player* 😢")
    except Exception as e:
        await ctx.send("*Puro encountered an error fetching Fortnite stats* 😔")

@bot.command(name='valorant')
async def valorant_stats(ctx, username: str, tagline: str):
    if not RIOT_API_KEY:
        await ctx.send("*Puro is sad* Riot API key is not configured!")
        return

    headers = {'X-Riot-Token': RIOT_API_KEY}
    
    try:
        # Get account info
        account_url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tagline}'
        account_response = requests.get(account_url, headers=headers)
        account_data = account_response.json()

        if account_response.status_code == 200:
            puuid = account_data['puuid']
            
            # Get ranked info
            ranked_url = f'https://api.henrikdev.xyz/valorant/v1/mmr/na/{username}/{tagline}'
            ranked_response = requests.get(ranked_url)
            ranked_data = ranked_response.json()

            embed = discord.Embed(title=f"Valorant Stats for {username}#{tagline}", color=0x000000)
            
            if ranked_response.status_code == 200:
                embed.add_field(name="Current Rank", value=ranked_data['data']['currenttierpatched'], inline=True)
                embed.add_field(name="Ranking in Tier", value=f"{ranked_data['data']['ranking_in_tier']}/100", inline=True)
                embed.add_field(name="MMR Change", value=ranked_data['data']['mmr_change_to_last_game'], inline=True)
            
            embed.set_footer(text="*Puro believes in you! 🎮*")
            await ctx.send(embed=embed)
        else:
            await ctx.send("*Puro couldn't find that Valorant player* 😢")
    except Exception as e:
        await ctx.send("*Puro encountered an error fetching Valorant stats* 😔")

@bot.command(name='lol')
async def league_stats(ctx, username: str, region: str = 'na1'):
    if not RIOT_API_KEY:
        await ctx.send("*Puro is sad* Riot API key is not configured!")
        return

    headers = {'X-Riot-Token': RIOT_API_KEY}
    
    try:
        # Get summoner info
        summoner_url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}'
        summoner_response = requests.get(summoner_url, headers=headers)
        summoner_data = summoner_response.json()

        if summoner_response.status_code == 200:
            summoner_id = summoner_data['id']
            
            # Get ranked info
            ranked_url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
            ranked_response = requests.get(ranked_url, headers=headers)
            ranked_data = ranked_response.json()

            embed = discord.Embed(title=f"League of Legends Stats for {username}", color=0x000000)
            
            if ranked_data:
                for queue in ranked_data:
                    if queue['queueType'] == 'RANKED_SOLO_5x5':
                        embed.add_field(name="Ranked Solo/Duo", value=f"{queue['tier']} {queue['rank']}", inline=True)
                        embed.add_field(name="LP", value=queue['leaguePoints'], inline=True)
                        embed.add_field(name="Win Rate", value=f"{int((queue['wins']/(queue['wins']+queue['losses']))*100)}%", inline=True)
                        embed.add_field(name="Wins/Losses", value=f"{queue['wins']}W/{queue['losses']}L", inline=True)
            
            embed.set_footer(text="*Puro cheers for your victories! 🏆*")
            await ctx.send(embed=embed)
        else:
            await ctx.send("*Puro couldn't find that League player* 😢")
    except Exception as e:
        await ctx.send("*Puro encountered an error fetching League stats* 😔")

@bot.command(name='base64encode')
async def encode_base64(ctx, *, text: str):
    encoded = base64.b64encode(text.encode()).decode()
    embed = discord.Embed(title="Base64 Encoder", color=0x000000)
    embed.add_field(name="Original Text", value=text, inline=False)
    embed.add_field(name="Encoded Text", value=encoded, inline=False)
    embed.set_footer(text="Powered by Puro's Lab 🧪")
    await ctx.send(embed=embed)

@bot.command(name='base64decode')
async def decode_base64(ctx, *, encoded: str):
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        embed = discord.Embed(title="Base64 Decoder", color=0x000000)
        embed.add_field(name="Encoded Text", value=encoded, inline=False)
        embed.add_field(name="Decoded Text", value=decoded, inline=False)
        embed.set_footer(text="Powered by Puro's Lab 🧪")
        await ctx.send(embed=embed)
    except:
        await ctx.send("*Puro scratches his head* That doesn't look like valid base64...")

@bot.command(name='genname')
async def generate_name(ctx):
    name = names.get_full_name()
    embed = discord.Embed(title="Random Name Generator", color=0x000000)
    embed.add_field(name="Generated Name", value=name, inline=False)
    embed.set_footer(text="Generated with love by Puro 🖤")
    await ctx.send(embed=embed)

@bot.command(name='genpass')
async def generate_password(ctx, length: int = 12):
    if length < 8 or length > 32:
        await ctx.send("*Puro suggests* Please choose a length between 8 and 32!")
        return
    
    # Generate a secure password using secrets module
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    
    # Send password in DM for security
    embed = discord.Embed(title="Password Generator", color=0x000000)
    embed.add_field(name="Generated Password", value=password, inline=False)
    embed.set_footer(text="Keep it secret, keep it safe! 🔒")
    await ctx.author.send(embed=embed)
    await ctx.send("*Puro whispers* I've sent you a secure password in DM! 🤫")

@bot.command(name='mccolors')
async def minecraft_colors(ctx):
    embed = discord.Embed(title="Minecraft Color Codes", color=0x000000)
    for code, color in MINECRAFT_COLORS.items():
        embed.add_field(name=code, value=color, inline=True)
    embed.set_footer(text="Minecraft colors, Puro style! 🎨")
    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
