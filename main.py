import discord
from discord import app_commands
from discord.ext import commands
import os
import random
import base64
import string
import secrets
import datetime
import re

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="p!", intents=intents)

# Constants
OWNER_ROLE_NAME = "Puro"
TRANSFUR_RESPONSES = [
    "*Puro sneaks up behind you and hugs you tight, covering you in black latex*",
    "*The black goo slowly envelops you, transforming you into a cute latex creature*",
    "*You feel the warm embrace of the dark latex, becoming one with Puro*",
    "*The transformation begins, your form shifting into a latex being*"
]

COMFORT_RESPONSES = [
    "Hey there! *Puro gives you a warm, comforting hug* Everything will be okay! 🖤",
    "*Puro sits next to you* I'm here to listen if you want to talk about anything!",
    "You're stronger than you think! *Puro offers a supportive pat* 🖤",
    "*Puro wraps you in a cozy blanket* Take all the time you need to rest.",
    "Remember, it's okay not to be okay. *Puro offers a shoulder to lean on*",
    "*Puro brings you some hot chocolate* Let's take a break together!",
    "You're not alone in this. *Puro sits quietly beside you* 🖤",
    "*Puro shows you cute pictures of latex creatures* Hope this makes you smile!",
    "Every storm passes eventually. *Puro holds your hand supportively*",
    "You're doing great, even if it doesn't feel like it! *Puro gives encouraging headpats*",
    "*Puro shares their favorite snacks with you* Sometimes a treat helps!",
    "Your feelings are valid. *Puro listens attentively* 🖤",
    "*Puro builds a cozy pillow fort* Want to hide from the world for a bit?",
    "Take a deep breath with me! *Puro demonstrates calming breathing* In... and out...",
    "*Puro brings you a warm towel* Let's wash away the stress!",
    "You deserve all the happiness in the world! *Puro gives you a gentle hug*",
    "*Puro shows you their collection of shiny things* Look at how they sparkle!",
    "Remember to be kind to yourself! *Puro offers encouraging squeaks*",
    "*Puro draws you a little heart* You're appreciated! 🖤",
    "It's okay to take breaks. *Puro helps you find a comfy spot to rest*"
]

MINECRAFT_COLORS = {
    "§0": {"name": "Black", "color": 0x000000},
    "§1": {"name": "Dark Blue", "color": 0x0000AA},
    "§2": {"name": "Dark Green", "color": 0x00AA00},
    "§3": {"name": "Dark Aqua", "color": 0x00AAAA},
    "§4": {"name": "Dark Red", "color": 0xAA0000},
    "§5": {"name": "Dark Purple", "color": 0xAA00AA},
    "§6": {"name": "Gold", "color": 0xFFAA00},
    "§7": {"name": "Gray", "color": 0xAAAAAA},
    "§8": {"name": "Dark Gray", "color": 0x555555},
    "§9": {"name": "Blue", "color": 0x5555FF},
    "§a": {"name": "Green", "color": 0x55FF55},
    "§b": {"name": "Aqua", "color": 0x55FFFF},
    "§c": {"name": "Red", "color": 0xFF5555},
    "§d": {"name": "Light Purple", "color": 0xFF55FF},
    "§e": {"name": "Yellow", "color": 0xFFFF55},
    "§f": {"name": "White", "color": 0xFFFFFF}
}

SOCIAL_LINKS = {
    "YouTube": "https://www.youtube.com/@SentakuuGaming",
    "Steam": "https://steamcommunity.com/id/Arionyx/",
    "Telegram": "https://t.me/SentakuuGaming",
    "Twitch": "https://www.twitch.tv/arionyxcz",
    "Minecraft": "Arionyxx"
}

@bot.event
async def on_ready():
    print(f'🐺 {bot.user} is ready to spread some latex love!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Game(name="/help for commands!"))

@bot.tree.command(name="comfort", description="Get a comforting message from Puro when you're feeling down")
async def comfort(interaction: discord.Interaction):
    response = random.choice(COMFORT_RESPONSES)
    embed = discord.Embed(
        description=response,
        color=0x000000
    )
    embed.set_author(name="Puro's Comfort Corner 🖤", icon_url=bot.user.avatar.url)
    embed.set_footer(text="Remember, you're never alone! 🤗")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="transfur", description="Get transfurred by Puro! (Requires Puro role)")
async def transfur(interaction: discord.Interaction):
    if discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        response = random.choice(TRANSFUR_RESPONSES)
        embed = discord.Embed(
            description=response,
            color=0x000000
        )
        embed.set_author(name="Puro's Latex Magic ✨", icon_url=bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("*Puro looks at you confused* Only my special friend can use this command!", ephemeral=True)

@bot.tree.command(name="mccolors", description="View Minecraft color codes with actual colors!")
async def minecraft_colors(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Minecraft Color Codes",
        description="Here are all the Minecraft color codes with examples!",
        color=0x000000
    )
    
    # Group colors into categories
    basics = ["§0", "§f", "§7", "§8"]
    warm_colors = ["§c", "§6", "§e", "§4"]
    cool_colors = ["§1", "§3", "§b", "§9"]
    nature = ["§2", "§a", "§5", "§d"]
    
    def create_color_field(codes):
        return "\n".join([f"`{code}` {MINECRAFT_COLORS[code]['name']}" for code in codes])
    
    embed.add_field(name="Basic Colors", value=create_color_field(basics), inline=True)
    embed.add_field(name="Warm Colors", value=create_color_field(warm_colors), inline=True)
    embed.add_field(name="Cool Colors", value=create_color_field(cool_colors), inline=True)
    embed.add_field(name="Nature Colors", value=create_color_field(nature), inline=True)
    
    embed.add_field(
        name="Formatting Codes",
        value="`§k` Obfuscated\n`§l` Bold\n`§m` Strikethrough\n`§n` Underline\n`§o` Italic\n`§r` Reset",
        inline=False
    )
    
    embed.set_footer(text="Minecraft colors, Puro style! 🎨")
    embed.set_author(name="Minecraft Color Guide", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="genname", description="Generate a custom name with a prefix")
async def generate_name(interaction: discord.Interaction, prefix: str):
    # Generate a random string of 6 characters (letters and numbers)
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Combine prefix and suffix with underscore
    generated_name = f"{prefix}_{suffix}"
    
    embed = discord.Embed(
        title="Custom Name Generator",
        color=0x000000
    )
    embed.add_field(name="Your Generated Name", value=f"`{generated_name}`", inline=False)
    embed.set_footer(text="Generated with love by Puro 🖤")
    embed.set_author(name="Name Generator", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="genpass", description="Generate a secure password")
async def generate_password(interaction: discord.Interaction, length: int = 16):
    if length < 8 or length > 32:
        await interaction.response.send_message("*Puro suggests* Please choose a length between 8 and 32!", ephemeral=True)
        return
    
    # Generate a secure password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Create password strength indicators
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    strength = sum([has_upper, has_lower, has_digit, has_special])
    strength_text = ["Weak 😟", "Moderate 🤔", "Strong 😊", "Very Strong 💪"][strength-1]
    
    # Send password in DM for security
    try:
        embed = discord.Embed(
            title="Secure Password Generator",
            description="Here's your secure password! Keep it safe! 🔒",
            color=0x000000
        )
        embed.add_field(name="Generated Password", value=f"||`{password}`||", inline=False)
        embed.add_field(name="Password Strength", value=strength_text, inline=True)
        embed.add_field(name="Length", value=str(length), inline=True)
        embed.set_footer(text="Keep it secret, keep it safe! 🔒")
        embed.set_author(name="Password Generator", icon_url=bot.user.avatar.url)
        
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("*Puro whispers* I've sent you a secure password in DM! 🤫", ephemeral=True)
    except:
        await interaction.response.send_message("*Puro looks worried* I couldn't send you a DM! Please enable DMs from server members.", ephemeral=True)

@bot.tree.command(name="base64encode", description="Encode text to base64")
async def encode_base64_cmd(interaction: discord.Interaction, text: str):
    encoded = base64.b64encode(text.encode()).decode()
    
    embed = discord.Embed(
        title="Base64 Encoder",
        color=0x000000
    )
    embed.add_field(name="Original Text", value=f"```{text}```", inline=False)
    embed.add_field(name="Encoded Text", value=f"```{encoded}```", inline=False)
    embed.set_footer(text="Powered by Puro's Lab 🧪")
    embed.set_author(name="Base64 Encoder", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="base64decode", description="Decode base64 text")
async def decode_base64_cmd(interaction: discord.Interaction, encoded: str):
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        embed = discord.Embed(
            title="Base64 Decoder",
            color=0x000000
        )
        embed.add_field(name="Encoded Text", value=f"```{encoded}```", inline=False)
        embed.add_field(name="Decoded Text", value=f"```{decoded}```", inline=False)
        embed.set_footer(text="Powered by Puro's Lab 🧪")
        embed.set_author(name="Base64 Decoder", icon_url=bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except:
        await interaction.response.send_message("*Puro scratches his head* That doesn't look like valid base64...", ephemeral=True)

@bot.tree.command(name="help", description="View all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Puro's Command List",
        description="Here are all the available commands! 🐺",
        color=0x000000
    )
    
    # Utility Commands
    utility_cmds = """
    `/base64encode` - Encode text to base64
    `/base64decode` - Decode base64 text
    `/genname` - Generate a custom name
    `/genpass` - Generate a secure password
    `/mccolors` - View Minecraft color codes
    `/socials` - View all my social media profiles
    """
    embed.add_field(name="🛠️ Utility", value=utility_cmds.strip(), inline=False)
    
    # Fun Commands - Only show transfur if user has Puro role
    if discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        fun_cmds = """
        `/comfort` - Get a comforting message when feeling down
        `/transfur` - Get transfurred by Puro!
        """
    else:
        fun_cmds = """
        `/comfort` - Get a comforting message when feeling down
        """
    embed.add_field(name="🎮 Fun", value=fun_cmds.strip(), inline=False)
    
    embed.set_footer(text="Use / to access commands! 💫")
    embed.set_author(name="Command Help", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="socials", description="View Sentakuu's social media profiles!")
async def social_media(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Sentakuu's Social Media",
        description="Come hang out with me on other platforms! 🎮",
        color=0x000000
    )
    
    # YouTube with special formatting
    embed.add_field(
        name="<:Youtube:1320208846022643822> YouTube",
        value=f"[SentakuuGaming]({SOCIAL_LINKS['YouTube']})",
        inline=True
    )
    
    # Twitch with stream note
    embed.add_field(
        name="<:Twitch:1320208844109910067> Twitch",
        value=f"[arionyxcz]({SOCIAL_LINKS['Twitch']})",
        inline=True
    )
    
    # Steam
    embed.add_field(
        name="<:steam:1320208840507002920> Steam",
        value=f"[Arionyx]({SOCIAL_LINKS['Steam']})",
        inline=True
    )
    
    # Telegram
    embed.add_field(
        name="<:Telegram:1320208842407280744> Telegram",
        value=f"[Sentakuu Gaming]({SOCIAL_LINKS['Telegram']})",
        inline=True
    )
    
    # Minecraft
    embed.add_field(
        name="<:Minecraft:1320208838896386108> Minecraft",
        value=f"`{SOCIAL_LINKS['Minecraft']}`",
        inline=True
    )
    
    embed.set_footer(text="Feel free to follow and say hi! 👋")
    embed.set_author(name="Social Media Links", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
