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

MINIGAME_COOLDOWNS = {}  # To prevent spam
COOLDOWN_TIME = 30  # seconds between games

SHOP_ITEMS = {
    "puros_cookie": {
        "name": "Puro's Cookie",
        "price": 100,
        "description": "A special cookie made by Puro himself! 🍪",
        "emoji": "🍪"
    },
    "puro_hat": {
        "name": "Puro's Hat",
        "price": 500,
        "description": "A stylish hat just like Puro's! 🎩",
        "emoji": "🎩"
    },
    "crystal_shard": {
        "name": "Crystal Shard",
        "price": 300,
        "description": "A shimmering piece of crystal! ✨",
        "emoji": "💎"
    },
    "latex_mask": {
        "name": "Latex Mask",
        "price": 750,
        "description": "A cute mask that looks like Puro! 🖤",
        "emoji": "🎭"
    },
    "science_book": {
        "name": "Laboratory Notes",
        "price": 250,
        "description": "Research notes from the facility! 📚",
        "emoji": "📚"
    }
}

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.level = 1
        self.xp = 0
        self.puro_coins = 0
        self.inventory = []  # List of item IDs
        self.last_game_time = 0

    def add_item(self, item_id):
        self.inventory.append(item_id)

    def has_item(self, item_id):
        return item_id in self.inventory

    def can_afford(self, price):
        return self.puro_coins >= price

user_profiles = {}

def get_user_profile(user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile(user_id)
    return user_profiles[user_id]

def check_cooldown(user_id):
    if user_id in MINIGAME_COOLDOWNS:
        time_diff = datetime.datetime.now().timestamp() - MINIGAME_COOLDOWNS[user_id]
        if time_diff < COOLDOWN_TIME:
            return int(COOLDOWN_TIME - time_diff)
    return 0

def update_cooldown(user_id):
    MINIGAME_COOLDOWNS[user_id] = datetime.datetime.now().timestamp()

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
        embed.set_author(name="Puro's Latex Magic ��", icon_url=bot.user.avatar.url)
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
    
    # Minigames
    games_cmds = """
    `/unscramble` - Unscramble Changed-themed words
    `/trivia` - Test your Changed knowledge
    `/guess` - Guess Puro's number (1-10)
    """
    embed.add_field(name="🎲 Minigames", value=games_cmds.strip(), inline=False)
    
    # Shop Commands
    shop_cmds = """
    `/shop` - Browse Puro's shop
    `/buy` - Purchase items from the shop
    `/inventory` - View your items
    """
    embed.add_field(name="🛍️ Shop", value=shop_cmds.strip(), inline=False)
    
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

@bot.tree.command(name="unscramble", description="Unscramble Changed-themed words!")
async def unscramble(interaction: discord.Interaction):
    # Check cooldown
    cooldown = check_cooldown(interaction.user.id)
    if cooldown > 0:
        await interaction.response.send_message(f"*Puro is still preparing the next game!* Please wait {cooldown} seconds! 🎮", ephemeral=True)
        return

    # Words related to Changed/Puro theme
    WORDS = [
        "latex", "puro", "changed", "transfur", "creature", "library", "crystal", "friend", 
        "dragon", "wolf", "tiger", "shark", "experiment", "science", "laboratory"
    ]
    
    # Pick a random word and scramble it
    word = random.choice(WORDS)
    scrambled = ''.join(random.sample(word, len(word)))
    
    embed = discord.Embed(
        title="🎮 Unscramble the Word!",
        description=f"Can you unscramble this word?\n\n**{scrambled}**\n\n*You have 30 seconds to answer!*",
        color=0x000000
    )
    embed.set_footer(text="Type your answer in chat!")
    embed.set_author(name="Puro's Word Game", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)
    update_cooldown(interaction.user.id)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        
        if msg.content.lower() == word:
            profile = get_user_profile(interaction.user.id)
            coins_earned = random.randint(10, 20)
            xp_earned = random.randint(5, 15)
            profile.puro_coins += coins_earned
            profile.xp += xp_earned
            
            win_embed = discord.Embed(
                title="🎉 Correct!",
                description=f"You unscrambled the word **{word}**!\n\nRewards:\n🪙 {coins_earned} PuroCoins\n✨ {xp_earned} XP",
                color=0x00FF00
            )
            win_embed.set_footer(text="Great job! Keep playing to earn more rewards!")
            await interaction.channel.send(embed=win_embed)
        else:
            lose_embed = discord.Embed(
                title="❌ Not quite!",
                description=f"The word was **{word}**. Try again next time!",
                color=0xFF0000
            )
            lose_embed.set_footer(text="Don't give up! Practice makes perfect!")
            await interaction.channel.send(embed=lose_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="⏰ Time's Up!",
            description=f"The word was **{word}**. Better luck next time!",
            color=0xFF0000
        )
        timeout_embed.set_footer(text="Try again! You'll get it!")
        await interaction.channel.send(embed=timeout_embed)

@bot.tree.command(name="trivia", description="Test your Changed knowledge!")
async def trivia(interaction: discord.Interaction):
    # Check cooldown
    cooldown = check_cooldown(interaction.user.id)
    if cooldown > 0:
        await interaction.response.send_message(f"*Puro is still preparing the next question!* Please wait {cooldown} seconds! 🎮", ephemeral=True)
        return

    TRIVIA_QUESTIONS = [
        {
            "question": "What color is Puro?",
            "answer": "black",
            "options": ["Black", "White", "Gray", "Blue"]
        },
        {
            "question": "Where does Puro first meet Colin?",
            "answer": "library",
            "options": ["Library", "Laboratory", "Warehouse", "School"]
        },
        {
            "question": "What type of creature is Puro?",
            "answer": "latex",
            "options": ["Latex", "Slime", "Ghost", "Shadow"]
        },
        {
            "question": "What game is Puro from?",
            "answer": "changed",
            "options": ["Changed", "Altered", "Transformed", "Shifted"]
        }
        # Add more questions as needed
    ]
    
    question = random.choice(TRIVIA_QUESTIONS)
    
    embed = discord.Embed(
        title="🎯 Changed Trivia",
        description=f"**{question['question']}**\n\n*You have 30 seconds to answer!*",
        color=0x000000
    )
    
    for i, option in enumerate(question['options'], 1):
        embed.add_field(name=f"Option {i}", value=option, inline=True)
    
    embed.set_footer(text="Type the answer in chat!")
    embed.set_author(name="Puro's Trivia Game", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)
    update_cooldown(interaction.user.id)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        
        if msg.content.lower() == question['answer']:
            profile = get_user_profile(interaction.user.id)
            coins_earned = random.randint(15, 25)
            xp_earned = random.randint(10, 20)
            profile.puro_coins += coins_earned
            profile.xp += xp_earned
            
            win_embed = discord.Embed(
                title="🎉 Correct Answer!",
                description=f"That's right!\n\nRewards:\n🪙 {coins_earned} PuroCoins\n✨ {xp_earned} XP",
                color=0x00FF00
            )
            win_embed.set_footer(text="Amazing knowledge! Keep it up!")
            await interaction.channel.send(embed=win_embed)
        else:
            lose_embed = discord.Embed(
                title="❌ Not Quite Right!",
                description=f"The correct answer was **{question['answer'].title()}**. Try again next time!",
                color=0xFF0000
            )
            lose_embed.set_footer(text="Keep learning about Changed!")
            await interaction.channel.send(embed=lose_embed)
    except TimeoutError:
        timeout_embed = discord.Embed(
            title="⏰ Time's Up!",
            description=f"The correct answer was **{question['answer'].title()}**.",
            color=0xFF0000
        )
        timeout_embed.set_footer(text="Be faster next time!")
        await interaction.channel.send(embed=timeout_embed)

@bot.tree.command(name="guess", description="Guess the number Puro is thinking of!")
async def guess_number(interaction: discord.Interaction, number: int):
    # Check cooldown
    cooldown = check_cooldown(interaction.user.id)
    if cooldown > 0:
        await interaction.response.send_message(f"*Puro is still thinking of a new number!* Please wait {cooldown} seconds! 🎮", ephemeral=True)
        return

    if number < 1 or number > 10:
        await interaction.response.send_message("*Puro tilts his head* Please guess a number between 1 and 10!", ephemeral=True)
        return

    correct = random.randint(1, 10)
    profile = get_user_profile(interaction.user.id)
    update_cooldown(interaction.user.id)

    embed = discord.Embed(
        title="🎲 Number Guessing Game",
        color=0x000000
    )

    if number == correct:
        coins_earned = random.randint(5, 15)
        xp_earned = random.randint(3, 10)
        profile.puro_coins += coins_earned
        profile.xp += xp_earned
        
        embed.description = f"🎉 **You got it!** The number was {correct}!\n\nRewards:\n🪙 {coins_earned} PuroCoins\n✨ {xp_earned} XP"
        embed.color = 0x00FF00
    else:
        embed.description = f"Not quite! The number was {correct}. Try again next time!"
        embed.color = 0xFF0000

    embed.set_footer(text="Keep playing to earn more rewards!")
    embed.set_author(name="Puro's Number Game", icon_url=bot.user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="Browse Puro's shop!")
async def shop(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    embed = discord.Embed(
        title="🏪 Puro's Shop",
        description="Welcome to my shop! Here's what I have for sale today:",
        color=0x000000
    )
    
    # Group items by price range
    budget_items = []
    medium_items = []
    premium_items = []
    
    for item_id, item in SHOP_ITEMS.items():
        if item["price"] <= 200:
            budget_items.append(item_id)
        elif item["price"] <= 500:
            medium_items.append(item_id)
        else:
            premium_items.append(item_id)
    
    def format_items(items):
        return "\n".join([
            f"{SHOP_ITEMS[item_id]['emoji']} **{SHOP_ITEMS[item_id]['name']}** - {SHOP_ITEMS[item_id]['price']} 🪙\n*{SHOP_ITEMS[item_id]['description']}*"
            for item_id in items
        ])
    
    if budget_items:
        embed.add_field(
            name="Budget Friendly 💫",
            value=format_items(budget_items),
            inline=False
        )
    
    if medium_items:
        embed.add_field(
            name="Popular Items ⭐",
            value=format_items(medium_items),
            inline=False
        )
    
    if premium_items:
        embed.add_field(
            name="Premium Collection 👑",
            value=format_items(premium_items),
            inline=False
        )
    
    embed.set_footer(text=f"Your Balance: 🪙 {profile.puro_coins} PuroCoins | Use /buy <item> to purchase!")
    embed.set_author(name="Shop", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy", description="Buy an item from Puro's shop!")
async def buy_item(interaction: discord.Interaction, item: str):
    profile = get_user_profile(interaction.user.id)
    
    # Convert input to shop item ID format
    item_id = item.lower().replace(" ", "_")
    
    if item_id not in SHOP_ITEMS:
        await interaction.response.send_message(
            "*Puro looks confused* I don't have that item in my shop! Use `/shop` to see what's available!",
            ephemeral=True
        )
        return
    
    shop_item = SHOP_ITEMS[item_id]
    
    if profile.has_item(item_id):
        await interaction.response.send_message(
            f"*Puro tilts his head* You already have a {shop_item['name']}!",
            ephemeral=True
        )
        return
    
    if not profile.can_afford(shop_item['price']):
        await interaction.response.send_message(
            f"*Puro looks sad* You need {shop_item['price']} PuroCoins for this item, but you only have {profile.puro_coins}!",
            ephemeral=True
        )
        return
    
    # Purchase the item
    profile.puro_coins -= shop_item['price']
    profile.add_item(item_id)
    
    embed = discord.Embed(
        title="🛍️ Purchase Successful!",
        description=f"You bought a {shop_item['emoji']} **{shop_item['name']}**!\n\n*{shop_item['description']}*",
        color=0x00FF00
    )
    embed.add_field(
        name="Price Paid",
        value=f"🪙 {shop_item['price']} PuroCoins",
        inline=True
    )
    embed.add_field(
        name="Remaining Balance",
        value=f"🪙 {profile.puro_coins} PuroCoins",
        inline=True
    )
    embed.set_footer(text="Thank you for shopping at Puro's! 🖤")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="inventory", description="View your inventory!")
async def view_inventory(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    embed = discord.Embed(
        title="🎒 Your Inventory",
        description="Here are all your items:",
        color=0x000000
    )
    
    if not profile.inventory:
        embed.description = "*Your inventory is empty!*\nVisit `/shop` to buy some items!"
    else:
        # Group items by type
        collectibles = []
        wearables = []
        consumables = []
        
        for item_id in profile.inventory:
            item = SHOP_ITEMS[item_id]
            if "hat" in item_id or "mask" in item_id:
                wearables.append(item)
            elif "cookie" in item_id:
                consumables.append(item)
            else:
                collectibles.append(item)
        
        def format_items(items):
            return "\n".join([
                f"{item['emoji']} **{item['name']}**\n*{item['description']}*"
                for item in items
            ])
        
        if wearables:
            embed.add_field(
                name="👕 Wearables",
                value=format_items(wearables),
                inline=False
            )
        
        if collectibles:
            embed.add_field(
                name="🏆 Collectibles",
                value=format_items(collectibles),
                inline=False
            )
        
        if consumables:
            embed.add_field(
                name="🍪 Consumables",
                value=format_items(consumables),
                inline=False
            )
    
    embed.set_footer(text=f"Balance: 🪙 {profile.puro_coins} PuroCoins")
    embed.set_author(name="Inventory", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
