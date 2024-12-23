import discord
from discord import app_commands
from discord.ext import commands, tasks
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

# Add guess number game configuration
GUESS_GAME_CONFIG = {
    "channel_id": None,
    "current_number": None,
    "active_game": False,
    "last_game_time": None,
    "min_number": 1,
    "max_number": 100,
    "winners": set(),
    "interval_minutes": 20  # Default interval
}

# Add giveaway configuration
GIVEAWAY_CONFIG = {
    "active_giveaways": {},  # Store active giveaways
    "ended_giveaways": set()  # Store ended giveaway message IDs
}

GIVEAWAY_EMOJI = "🎉"
GIVEAWAY_PURO_GIF = "https://media1.tenor.com/m/E5_AUOTIL2kAAAAd/puro-changed.gif"

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
    "It's okay to take breaks. *Puro helps you find a comfy spot to rest*",
    "*Puro creates a small light show with his latex powers* Look at the pretty patterns! ✨",
    "You matter more than you know. *Puro nuzzles you gently* 🖤",
    "*Puro brings out his collection of soft plushies* Want to cuddle with one?",
    "The world is better with you in it! *Puro dances happily* 💫",
    "*Puro makes funny faces to cheer you up* Sometimes laughter is the best medicine!",
    "You've got this! *Puro gives you a confidence-boosting high five* ✋",
    "*Puro shows you his favorite hiding spots in the library* Sometimes we all need a quiet place.",
    "Your best is always enough. *Puro hugs you protectively* 🖤",
    "*Puro creates a small latex bubble around you both* Safe and sound!",
    "Tomorrow is a new day. *Puro watches the stars with you* ⭐",
    "*Puro brings you a collection of his favorite books* Reading always helps me feel better!",
    "You're braver than you believe! *Puro gives you a proud smile* 💪",
    "*Puro creates a tiny latex butterfly* Watch it flutter around!",
    "It's okay to lean on others. *Puro offers his support* We're here for you!",
    "*Puro shows you his secret collection of crystals* They shine just like your spirit! ✨",
    "You bring light to others' lives. *Puro beams with pride* 🌟",
    "*Puro creates a small latex rain shelter* I'll keep you safe and dry!",
    "Your struggles don't define you. *Puro offers a reassuring pat* 🖤",
    "*Puro shares stories of his adventures* Sometimes a distraction helps!",
    "You're making progress, even if you can't see it. *Puro cheers you on* 🎉",
    "*Puro creates a cozy latex hammock* Let's relax together! 🌅",
    "Your heart is strong. *Puro places a paw over his heart* I believe in you! 💝",
    "*Puro shows you his collection of glowing crystals* Light always finds a way through darkness ✨",
    "You're doing better than you think. *Puro gives an encouraging tail wag* 🖤",
    "*Puro creates a small latex garden* Watch how things grow and change! 🌱",
    "Every step forward counts. *Puro walks beside you supportively* 🐾",
    "*Puro shares his favorite stargazing spot* Sometimes looking up helps put things in perspective! 🌟",
    "You have a beautiful soul. *Puro's eyes sparkle with admiration* ✨",
    "*Puro creates a latex rainbow* After the rain comes color! 🌈",
    "Take things one moment at a time. *Puro offers gentle support* 🖤",
    "*Puro shows you his collection of precious memories* You're creating beautiful ones too! 📱",
    "Your presence makes the world warmer. *Puro snuggles close* 💕",
    "*Puro creates a protective latex shield* Nothing can harm you here! 🛡️",
    "You're stronger with each passing day. *Puro flexes playfully* 💪",
    "*Puro shares his secret stash of comfort items* Pick anything you like! 🎁",
    "The darkness won't last forever. *Puro's markings glow softly* ✨",
    "*Puro creates a latex swing* Sometimes you need to see things from a new perspective! 🎪",
    "Your feelings matter. *Puro listens with full attention* 🖤",
    "*Puro shows you his collection of healing crystals* Feel their calming energy! 💎",
    "You're never too broken to heal. *Puro demonstrates his shapeshifting* See? Change is possible! ✨",
    "*Puro creates a latex cloud to rest on* Float away from your worries for a bit! ☁️",
    "Your journey is unique. *Puro traces patterns in the air* No two paths are the same! 🌟",
    "*Puro shows you his favorite meditation spot* Find your inner peace! 🧘",
    "You're worthy of love and support. *Puro hugs you tight* 💝",
    "*Puro creates a latex carousel* Let's take a break and have some fun! 🎠",
    "Each breath is a new beginning. *Puro demonstrates deep breathing* 🌬️",
    "*Puro shares his collection of inspiring notes* Words can heal! 📝",
    "You're not defined by your struggles. *Puro shows his battle scars proudly* 💫",
    "*Puro creates a latex fountain* Listen to the calming sounds! 🎵",
    "Your light never truly dims. *Puro's markings pulse with warmth* ✨",
    "*Puro creates a cozy latex nest* Sometimes we all need a safe space to rest! 🏠",
    "Your strength inspires others. *Puro looks at you with admiration* 💫",
    "*Puro shows you his collection of dream catchers* Let's catch some happy dreams! 🌙",
    "Every small victory counts. *Puro celebrates with a little dance* 🎊",
    "*Puro creates a latex lantern* Let's light up the darkness together! 🏮",
    "You're growing stronger each day. *Puro measures your height playfully* 📏",
    "*Puro shares his favorite comfort food* Food always tastes better with friends! 🍜",
    "Your smile brightens everyone's day. *Puro beams happily* ☀️",
    "*Puro creates a latex umbrella* I'll help keep the rain away! ☔",
    "Time heals all wounds. *Puro gently bandages your heart* 💝",
    "*Puro shows you his collection of lucky charms* Everyone needs a little extra luck! 🍀",
    "You're braver than you realize. *Puro gives you a courage medal* 🏅",
    "*Puro creates a latex bridge* I'll help you cross any obstacle! 🌉",
    "Your kindness touches hearts. *Puro shares his favorite memory of you* 💖",
    "*Puro builds a latex castle* You deserve to feel like royalty! 👑",
    "Keep shining bright. *Puro's markings glow in harmony with yours* ✨",
    "*Puro creates a latex telescope* Let's look at the stars and dream big! 🔭",
    "Your potential is limitless. *Puro shows you a mirror reflecting your inner light* 💫",
    "*Puro makes a latex kaleidoscope* Life is full of beautiful patterns! 🎨",
    "You make the world a better place. *Puro creates a tiny latex world* 🌍",
    "*Puro shows you his collection of positive affirmations* Let's read them together! 📖",
    "Your heart is pure gold. *Puro creates a golden latex crown* 👑",
    "*Puro builds a latex treehouse* Sometimes we need to rise above our troubles! 🌳",
    "You're an inspiration. *Puro creates a wall of your achievements* 🏆",
    "*Puro shows you his collection of healing herbs* Nature has many ways to comfort us! 🌿",
    "Your spirit is unbreakable. *Puro demonstrates his resilient latex form* 💪",
    "*Puro creates a latex time capsule* Let's store today's worries away! ⏳",
    "You're capable of amazing things. *Puro shows you his wall of possibilities* 🌟",
    "*Puro makes a latex music box* Let's listen to soothing melodies! 🎵",
    "Your journey is worth celebrating. *Puro throws confetti made of latex* 🎉"
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

TITLES = {
    "newcomer": {
        "name": "Newcomer",
        "description": "Just arrived at the facility!",
        "requirement": "Default title for new users"
    },
    "changed_fan": {
        "name": "Changed Fan",
        "description": "A true fan of Changed!",
        "requirement": "Reach level 5"
    },
    "latex_friend": {
        "name": "Latex Friend",
        "description": "Friend to all latex creatures!",
        "requirement": "Win 10 minigames"
    },
    "puro_bestie": {
        "name": "Puro's Bestie",
        "description": "Puro's closest friend!",
        "requirement": "Reach level 10"
    },
    "rich_collector": {
        "name": "Rich Collector",
        "description": "Owns many precious items!",
        "requirement": "Own 5 items from the shop"
    }
}

BADGES = {
    "minigame_master": {
        "name": "Minigame Master",
        "emoji": "🎮",
        "description": "Won 50 minigames",
        "secret": False
    },
    "rich_puro": {
        "name": "Wealthy",
        "emoji": "💰",
        "description": "Earned 1000 PuroCoins",
        "secret": False
    },
    "shopaholic": {
        "name": "Shopaholic",
        "emoji": "🛍️",
        "description": "Bought 10 items from the shop",
        "secret": False
    },
    "quiz_genius": {
        "name": "Quiz Genius",
        "emoji": "🎯",
        "description": "Got 10 trivia questions correct",
        "secret": False
    },
    "secret_finder": {
        "name": "Secret Finder",
        "emoji": "🔍",
        "description": "???",
        "secret": True
    }
}

BANNERS = {
    "default": {
        "name": "Laboratory",
        "url": "https://media.discordapp.net/attachments/1184577147927277698/1184577149555298394/lab.png",
        "description": "The mysterious facility",
        "price": 0
    },
    "library": {
        "name": "Library",
        "url": "https://media.discordapp.net/attachments/1184577147927277698/1184577149819531264/library.png",
        "description": "Where it all began",
        "price": 1000
    },
    "crystal": {
        "name": "Crystal Cave",
        "url": "https://media.discordapp.net/attachments/1184577147927277698/1184577150075564122/crystal.png",
        "description": "Shimmering crystals everywhere",
        "price": 1500
    },
    "dark_latex": {
        "name": "Dark Latex",
        "url": "https://media.discordapp.net/attachments/1184577147927277698/1184577150331789332/dark_latex.png",
        "description": "Home of the dark latex beasts",
        "price": 2000
    }
}

DAILY_REWARDS = {
    1: {"coins": 100, "xp": 50, "description": "First day reward!"},
    2: {"coins": 150, "xp": 75, "description": "Two days in a row!"},
    3: {"coins": 200, "xp": 100, "description": "Three-day streak!"},
    4: {"coins": 250, "xp": 125, "description": "Four days strong!"},
    5: {"coins": 300, "xp": 150, "description": "Five-day dedication!"},
    6: {"coins": 350, "xp": 175, "description": "Almost a week!"},
    7: {"coins": 500, "xp": 250, "description": "Full week achieved!"}
}

ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps",
        "description": "Claim your first daily reward",
        "emoji": "🐾",
        "reward_coins": 50,
        "reward_xp": 25,
        "secret": False
    },
    "social_butterfly": {
        "name": "Social Butterfly",
        "description": "Check out all social media links",
        "emoji": "🦋",
        "reward_coins": 100,
        "reward_xp": 50,
        "secret": False
    },
    "shopkeeper_friend": {
        "name": "Shopkeeper's Friend",
        "description": "Buy your first item from the shop",
        "emoji": "🛍️",
        "reward_coins": 75,
        "reward_xp": 35,
        "secret": False
    },
    "word_master": {
        "name": "Word Master",
        "description": "Win 5 unscramble games",
        "emoji": "📝",
        "reward_coins": 150,
        "reward_xp": 75,
        "secret": False
    },
    "trivia_expert": {
        "name": "Trivia Expert",
        "description": "Answer 10 trivia questions correctly",
        "emoji": "🎯",
        "reward_coins": 200,
        "reward_xp": 100,
        "secret": False
    },
    "lucky_guesser": {
        "name": "Lucky Guesser",
        "description": "Win the number guessing game 3 times",
        "emoji": "🎲",
        "reward_coins": 125,
        "reward_xp": 60,
        "secret": False
    },
    "dedicated_fan": {
        "name": "Dedicated Fan",
        "description": "Maintain a 7-day daily reward streak",
        "emoji": "⭐",
        "reward_coins": 300,
        "reward_xp": 150,
        "secret": False
    },
    "fashion_lover": {
        "name": "Fashion Lover",
        "description": "Own 3 different wearable items",
        "emoji": "👔",
        "reward_coins": 175,
        "reward_xp": 85,
        "secret": False
    },
    "rich_puro": {
        "name": "Rich Puro",
        "description": "Have 1000 PuroCoins at once",
        "emoji": "💰",
        "reward_coins": 250,
        "reward_xp": 125,
        "secret": False
    },
    "secret_hunter": {
        "name": "???",
        "description": "Find all secret achievements",
        "emoji": "🔍",
        "reward_coins": 500,
        "reward_xp": 250,
        "secret": True
    }
}

# Add Puro comfort GIFs at the top with other constants
PURO_COMFORT_GIFS = [
    "https://media1.tenor.com/m/S_pnQE1wbNwAAAAd/changed-puro.gif",  # Puro waving
    "https://media1.tenor.com/m/E5_AUOTIL2kAAAAd/puro-changed.gif",  # Puro dancing
    "https://media.tenor.com/fMxpOHq7hQ0AAAAj/pet-pet-puro.gif",  # Pet pet Puro
    "https://media.tenor.com/B4c8gNAbeH0AAAAj/puro-changed.gif",  # Puro happy
    "https://media1.tenor.com/m/0O2Eo4f2oc0AAAAd/puro-changed.gif"   # Puro cute
]

# Constants at the top of the file
COIN_EMOJI = "💰"  # Money bag emoji
HUG_EMOJI = "🤗"  # Hug emoji for comfort messages
STREAK_EMOJI = "⭐"  # Star emoji for streaks
FILLED_STREAK_EMOJI = "🌟"  # Filled star for active streak

# Update comfort tips
COMFORT_TIPS = [
    f"{HUG_EMOJI} Reach out to friends",
    "🧘 Take deep breaths",
    "🎵 Listen to music",
    "🚶 Go for a walk",
    "💭 Write your feelings"
]

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.level = 1
        self.xp = 0
        self.puro_coins = 0
        self.inventory = []
        self.last_game_time = 0
        self.title = "newcomer"  # Default title
        self.badges = set()  # Set of earned badges
        self.banner = "default"  # Current banner
        self.owned_banners = {"default"}  # Set of owned banners
        self.games_won = 0  # Track game wins for badges
        self.trivia_correct = 0  # Track correct trivia answers
        self.last_daily = None  # Last daily reward claim time
        self.daily_streak = 0  # Current streak of daily rewards
        self.achievements = set()  # Completed achievements
        self.unscramble_wins = 0
        self.guess_wins = 0
        self.wearables_owned = 0

    def add_item(self, item_id):
        self.inventory.append(item_id)

    def has_item(self, item_id):
        return item_id in self.inventory

    def can_afford(self, price):
        return self.puro_coins >= price

    def add_xp(self, amount):
        self.xp += amount
        # Check for level up
        next_level = self.level * 100  # XP needed for next level
        while self.xp >= next_level:
            self.level += 1
            self.xp -= next_level
            next_level = self.level * 100
            # Check for level-based titles
            if self.level >= 5:
                self.unlock_title("changed_fan")
            if self.level >= 10:
                self.unlock_title("puro_bestie")

    def unlock_title(self, title_id):
        if title_id in TITLES:
            self.title = title_id

    def earn_badge(self, badge_id):
        if badge_id in BADGES and not BADGES[badge_id]["secret"]:
            self.badges.add(badge_id)

    def buy_banner(self, banner_id):
        if banner_id in BANNERS and self.puro_coins >= BANNERS[banner_id]["price"]:
            self.puro_coins -= BANNERS[banner_id]["price"]
            self.owned_banners.add(banner_id)
            return True
        return False

    def set_banner(self, banner_id):
        if banner_id in self.owned_banners:
            self.banner = banner_id
            return True
        return False

    def can_claim_daily(self):
        if not self.last_daily:
            return True
        
        now = datetime.datetime.now()
        last_claim = datetime.datetime.fromtimestamp(self.last_daily)
        time_diff = now - last_claim
        
        # Check if it's been between 20-28 hours since last claim
        # This gives a 4-hour grace period for maintaining streaks
        hours_diff = time_diff.total_seconds() / 3600
        return hours_diff >= 20

    def should_reset_streak(self):
        if not self.last_daily:
            return False
        
        now = datetime.datetime.now()
        last_claim = datetime.datetime.fromtimestamp(self.last_daily)
        time_diff = now - last_claim
        hours_diff = time_diff.total_seconds() / 3600
        
        # Reset streak if more than 28 hours have passed
        return hours_diff > 28

    def claim_daily(self):
        now = datetime.datetime.now()
        
        # Reset streak if too much time has passed
        if self.should_reset_streak():
            self.daily_streak = 0
        
        # Increment streak (max 7 days)
        self.daily_streak = min(self.daily_streak + 1, 7)
        
        # Get rewards for current streak
        rewards = DAILY_REWARDS[self.daily_streak]
        
        # Apply rewards
        self.puro_coins += rewards["coins"]
        self.add_xp(rewards["xp"])
        
        # Update last claim time
        self.last_daily = now.timestamp()
        
        return rewards

    def check_achievements(self):
        earned = []
        
        # First Steps
        if "first_steps" not in self.achievements and self.last_daily is not None:
            earned.append(self.earn_achievement("first_steps"))
        
        # Word Master
        if "word_master" not in self.achievements and self.unscramble_wins >= 5:
            earned.append(self.earn_achievement("word_master"))
        
        # Trivia Expert
        if "trivia_expert" not in self.achievements and self.trivia_correct >= 10:
            earned.append(self.earn_achievement("trivia_expert"))
        
        # Lucky Guesser
        if "lucky_guesser" not in self.achievements and self.guess_wins >= 3:
            earned.append(self.earn_achievement("lucky_guesser"))
        
        # Dedicated Fan
        if "dedicated_fan" not in self.achievements and self.daily_streak >= 7:
            earned.append(self.earn_achievement("dedicated_fan"))
        
        # Rich Puro
        if "rich_puro" not in self.achievements and self.puro_coins >= 1000:
            earned.append(self.earn_achievement("rich_puro"))
        
        # Fashion Lover
        wearables = sum(1 for item in self.inventory if "hat" in item or "mask" in item)
        if "fashion_lover" not in self.achievements and wearables >= 3:
            earned.append(self.earn_achievement("fashion_lover"))
        
        return earned

    def earn_achievement(self, achievement_id):
        if achievement_id not in self.achievements and achievement_id in ACHIEVEMENTS:
            self.achievements.add(achievement_id)
            achievement = ACHIEVEMENTS[achievement_id]
            
            # Apply rewards
            self.puro_coins += achievement["reward_coins"]
            self.add_xp(achievement["reward_xp"])
            
            return achievement
        return None

    def add_coins(self, amount):
        """Add coins to the user's balance"""
        self.puro_coins += amount
        # Check for rich_puro achievement
        if self.puro_coins >= 1000:
            self.earn_badge("rich_puro")

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
    gif_url = random.choice(PURO_COMFORT_GIFS)
    
    embed = discord.Embed(
        title="🖤 Puro's Comfort Corner",
        description=f"# {interaction.user.name}...\n\n{response}",
        color=0x2b2d31  # Discord dark theme color
    )
    
    # Add a random encouraging quote
    quotes = [
        "Every storm runs out of rain ✨",
        "You're stronger than you know 💪",
        "This too shall pass 🌟",
        "Take it one step at a time 🐾",
        "You're not alone in this journey 🤗"
    ]
    embed.add_field(
        name="Remember...",
        value=random.choice(quotes),
        inline=False
    )
    
    # Add tips for self-care
    tips = [
        "🫂 Reach out to friends",
        "🧘 Take deep breaths",
        "🎵 Listen to music",
        "🚶 Go for a walk",
        "💭 Write your feelings"
    ]
    embed.add_field(
        name="Self-Care Tips",
        value="\n".join(random.sample(tips, 3)),  # Show 3 random tips
        inline=False
    )
    
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_image(url=gif_url)
    embed.set_footer(text="You're valued and appreciated! 🖤")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="transfur", description="Get transfurred by Puro! (Requires Puro role)")
async def transfur(interaction: discord.Interaction):
    if discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        response = random.choice(TRANSFUR_RESPONSES)
        embed = discord.Embed(
            description=response,
            color=0x000000
        )
        embed.set_author(name="Puro's Latex Magic", icon_url=bot.user.avatar.url)
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
    strength_text = ["Weak ���", "Moderate 🤔", "Strong 😊", "Very Strong 💪"][strength-1]
    
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
    try:
        # Defer the response since building the help embed might take a moment
        await interaction.response.defer(ephemeral=False)
        
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
        `/daily` - Claim your daily reward!
        """
        embed.add_field(name="🎲 Minigames", value=games_cmds.strip(), inline=False)
        
        # Shop Commands
        shop_cmds = """
        `/shop` - Browse Puro's shop
        `/buy` - Purchase items from the shop
        `/inventory` - View your items
        """
        embed.add_field(name="🛍️ Shop", value=shop_cmds.strip(), inline=False)
        
        # Profile Commands
        profile_cmds = """
        `/profile` - View your profile
        `/titles` - View available titles
        `/settitle` - Change your title
        `/banners` - View available banners
        `/buybanner` - Buy a new banner
        `/setbanner` - Set your banner
        `/achievements` - View your achievements
        """
        embed.add_field(name="👤 Profile", value=profile_cmds.strip(), inline=False)
        
        # Giveaway Commands - Only show if user has admin permissions
        if interaction.user.guild_permissions.administrator:
            giveaway_cmds = """
            `/giveaway` - Start a new giveaway
            `/reroll` - Reroll a giveaway winner
            `/setguessinterval` - Set guess game interval
            `/setguesschannel` - Set guess game channel
            `/stopguess` - Stop the guess game
            """
            embed.add_field(name="🎉 Giveaway", value=giveaway_cmds.strip(), inline=False)
        
        embed.set_footer(text="Use / to access commands! 💫")
        embed.set_author(name="Command Help", icon_url=bot.user.avatar.url)
        
        # Use followup instead of response
        await interaction.followup.send(embed=embed)
        
    except discord.NotFound:
        # If the interaction is no longer valid, we'll just pass
        pass
    except Exception as e:
        # Log any other errors
        print(f"Error in help command: {str(e)}")
        try:
            await interaction.followup.send("An error occurred while showing the help menu. Please try again!", ephemeral=True)
        except:
            pass

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
            
            # Use proper methods for rewards
            profile.add_coins(coins_earned)
            profile.add_xp(xp_earned)
            profile.unscramble_wins += 1
            
            # Check achievements
            new_achievements = profile.check_achievements()
            
            win_embed = discord.Embed(
                title="🎉 Correct!",
                description=f"You unscrambled the word **{word}**!\n\nRewards:\n{COIN_EMOJI} {coins_earned} PuroCoins\n✨ {xp_earned} XP",
                color=0x00FF00
            )
            win_embed.set_footer(text="Great job! Keep playing to earn more rewards!")
            await interaction.channel.send(embed=win_embed)
            
            # Show achievement notifications
            if new_achievements:
                for achievement in new_achievements:
                    reward_embed = discord.Embed(
                        title="🎉 Achievement Unlocked!",
                        description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                        color=0x00FF00
                    )
                    reward_embed.add_field(
                        name="Rewards",
                        value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                        inline=False
                    )
                    await interaction.channel.send(embed=reward_embed)
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
            
            # Use proper methods for rewards
            profile.add_coins(coins_earned)
            profile.add_xp(xp_earned)
            profile.trivia_correct += 1
            
            # Check achievements
            new_achievements = profile.check_achievements()
            
            win_embed = discord.Embed(
                title="🎉 Correct Answer!",
                description=f"That's right!\n\nRewards:\n{COIN_EMOJI} {coins_earned} PuroCoins\n✨ {xp_earned} XP",
                color=0x00FF00
            )
            win_embed.set_footer(text="Amazing knowledge! Keep it up!")
            await interaction.channel.send(embed=win_embed)
            
            # Show achievement notifications
            if new_achievements:
                for achievement in new_achievements:
                    reward_embed = discord.Embed(
                        title="🎉 Achievement Unlocked!",
                        description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                        color=0x00FF00
                    )
                    reward_embed.add_field(
                        name="Rewards",
                        value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                        inline=False
                    )
                    await interaction.channel.send(embed=reward_embed)
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
        profile.guess_wins += 1  # Track wins for achievements
        
        # Check achievements
        new_achievements = profile.check_achievements()
        
        embed.description = f"🎉 **You got it!** The number was {correct}!\n\nRewards:\n{COIN_EMOJI} {coins_earned} PuroCoins\n✨ {xp_earned} XP"
        embed.color = 0x00FF00
        
        # Show achievement notifications after the guess result
        if new_achievements:
            for achievement in new_achievements:
                reward_embed = discord.Embed(
                    title="🎉 Achievement Unlocked!",
                    description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                    color=0x00FF00
                )
                reward_embed.add_field(
                    name="Rewards",
                    value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                    inline=False
                )
                await interaction.channel.send(embed=reward_embed)
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
            f"{SHOP_ITEMS[item_id]['emoji']} **{SHOP_ITEMS[item_id]['name']}** - {SHOP_ITEMS[item_id]['price']} {COIN_EMOJI}\n*{SHOP_ITEMS[item_id]['description']}*"
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
    
    embed.set_footer(text=f"Your Balance: {COIN_EMOJI} {profile.puro_coins} PuroCoins | Use /buy <item> to purchase!")
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
        value=f"{COIN_EMOJI} {shop_item['price']} PuroCoins",
        inline=True
    )
    embed.add_field(
        name="Remaining Balance",
        value=f"{COIN_EMOJI} {profile.puro_coins} PuroCoins",
        inline=True
    )
    embed.set_footer(text="Thank you for shopping at Puro's! 🖤")
    
    await interaction.response.send_message(embed=embed)

@buy_item.autocomplete('item')
async def buy_item_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    items = []
    for item_id, item in SHOP_ITEMS.items():
        name = f"{item['emoji']} {item['name']} - {item['price']} {COIN_EMOJI}"
        if current.lower() in name.lower():
            items.append(app_commands.Choice(name=name, value=item_id))
    return items[:25]  # Discord limits to 25 choices

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
    
    embed.set_footer(text=f"Balance: {COIN_EMOJI} {profile.puro_coins} PuroCoins")
    embed.set_author(name="Inventory", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="profile", description="View your or another user's profile!")
async def view_profile(interaction: discord.Interaction, user: discord.Member = None):
    target_user = user or interaction.user
    profile = get_user_profile(target_user.id)
    
    # Calculate level progress
    next_level_xp = profile.level * 100
    progress = int((profile.xp / next_level_xp) * 20)  # Using 20 blocks for smoother bar
    progress_bar = "▰" * progress + "▱" * (20 - progress)
    
    # Create main embed
    embed = discord.Embed(color=0x2b2d31)  # Discord dark theme color
    
    # Set banner if available
    if profile.banner in BANNERS:
        embed.set_image(url=BANNERS[profile.banner]["url"])
    
    # Profile Header
    header = f"# {target_user.name}'s Profile\n"
    header += f"> {TITLES[profile.title]['name']} • Level {profile.level}\n"
    header += f"> *{TITLES[profile.title]['description']}*\n\n"
    
    # Level and XP with custom progress bar
    header += "### Level Progress\n"
    header += f"`{progress_bar}` {profile.xp}/{next_level_xp} XP\n\n"
    
    # Stats in a clean format with proper emojis
    header += "```\n"
    header += f"PuroCoins : {profile.puro_coins:,} 💰\n"
    header += f"Games Won : {profile.games_won:,} 🎮\n"
    header += f"Items    : {len(profile.inventory):,} 🎒\n"
    header += "```\n"
    
    embed.description = header
    
    # Badges Section
    if profile.badges:
        badges_text = " ".join([BADGES[badge]["emoji"] for badge in profile.badges])
        embed.add_field(
            name="🏆 Badges",
            value=badges_text or "No badges yet",
            inline=False
        )
    
    # Recent Achievements
    recent_achievements = list(profile.achievements)[-3:]  # Get last 3 achievements
    if recent_achievements:
        achievements_text = "\n".join([
            f"{ACHIEVEMENTS[ach]['emoji']} **{ACHIEVEMENTS[ach]['name']}**"
            for ach in recent_achievements
        ])
        embed.add_field(
            name="🌟 Recent Achievements",
            value=achievements_text,
            inline=False
        )
    
    # Daily Streak if any
    if profile.daily_streak > 0:
        streak_bar = f"{FILLED_STREAK_EMOJI} " * profile.daily_streak + f"{STREAK_EMOJI} " * (7 - profile.daily_streak)
        embed.add_field(
            name="📅 Daily Streak",
            value=f"Day {profile.daily_streak} of 7\n{streak_bar}",
            inline=False
        )
    
    # Set thumbnail and footer
    embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)
    join_date = target_user.created_at.strftime("%B %d, %Y")
    embed.set_footer(
        text=f"Member since: {join_date}",
        icon_url=bot.user.avatar.url
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="titles", description="View and select your titles!")
async def view_titles(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    embed = discord.Embed(
        title="Available Titles",
        description="Here are all the titles you can earn:",
        color=0x000000
    )
    
    for title_id, title in TITLES.items():
        # Add 🎯 if it's the current title
        current = "🎯 " if profile.title == title_id else ""
        embed.add_field(
            name=f"{current}{title['name']}",
            value=f"*{title['description']}*\nRequirement: {title['requirement']}",
            inline=False
        )
    
    embed.set_footer(text="Use /settitle <title> to change your title!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="settitle", description="Set your active title!")
async def set_title(interaction: discord.Interaction, title: str):
    profile = get_user_profile(interaction.user.id)
    title_id = title.lower().replace(" ", "_")
    
    if title_id not in TITLES:
        await interaction.response.send_message("*Puro looks confused* That title doesn't exist!", ephemeral=True)
        return
    
    # Check if user meets requirements
    if title_id == "changed_fan" and profile.level < 5:
        await interaction.response.send_message("You need to reach level 5 to use this title!", ephemeral=True)
        return
    elif title_id == "puro_bestie" and profile.level < 10:
        await interaction.response.send_message("You need to reach level 10 to use this title!", ephemeral=True)
        return
    elif title_id == "latex_friend" and profile.games_won < 10:
        await interaction.response.send_message("You need to win 10 games to use this title!", ephemeral=True)
        return
    elif title_id == "rich_collector" and len(profile.inventory) < 5:
        await interaction.response.send_message("You need to own 5 items to use this title!", ephemeral=True)
        return
    
    profile.title = title_id
    await interaction.response.send_message(f"Your title has been changed to **{TITLES[title_id]['name']}**!")

@set_title.autocomplete('title')
async def title_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    profile = get_user_profile(interaction.user.id)
    titles = []
    for title_id, title in TITLES.items():
        # Check requirements
        available = True
        if title_id == "changed_fan" and profile.level < 5:
            available = False
        elif title_id == "puro_bestie" and profile.level < 10:
            available = False
        elif title_id == "latex_friend" and profile.games_won < 10:
            available = False
        elif title_id == "rich_collector" and len(profile.inventory) < 5:
            available = False
        
        name = f"{title['name']} - {title['description']}"
        if not available:
            name += " (🔒 Locked)"
        
        if current.lower() in name.lower():
            titles.append(app_commands.Choice(name=name, value=title_id))
    return titles[:25]

@bot.tree.command(name="banners", description="View and buy profile banners!")
async def view_banners(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    embed = discord.Embed(
        title="Profile Banners",
        description="Customize your profile with these awesome banners!",
        color=0x000000
    )
    
    for banner_id, banner in BANNERS.items():
        # Add indicators for owned/equipped banners
        status = "✨ " if banner_id == profile.banner else "✅ " if banner_id in profile.owned_banners else ""
        price_text = "Owned" if banner_id in profile.owned_banners else f"{COIN_EMOJI} {banner['price']} PuroCoins"
        
        embed.add_field(
            name=f"{status}{banner['name']}",
            value=f"*{banner['description']}*\nPrice: {price_text}",
            inline=False
        )
    
    embed.set_footer(text="Use /setbanner <name> to equip a banner or /buybanner <name> to buy one!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buybanner", description="Buy a new profile banner!")
async def buy_banner(interaction: discord.Interaction, banner: str):
    profile = get_user_profile(interaction.user.id)
    banner_id = banner.lower().replace(" ", "_")
    
    if banner_id not in BANNERS:
        await interaction.response.send_message("*Puro looks confused* That banner doesn't exist!", ephemeral=True)
        return
    
    if banner_id in profile.owned_banners:
        await interaction.response.send_message("You already own this banner!", ephemeral=True)
        return
    
    banner_data = BANNERS[banner_id]
    if profile.buy_banner(banner_id):
        embed = discord.Embed(
            title="🎉 Banner Purchased!",
            description=f"You bought the **{banner_data['name']}** banner!\n\n*{banner_data['description']}*",
            color=0x00FF00
        )
        embed.add_field(name="Price Paid", value=f"{COIN_EMOJI} {banner_data['price']} PuroCoins")
        embed.add_field(name="Remaining Balance", value=f"{COIN_EMOJI} {profile.puro_coins} PuroCoins")
        embed.set_footer(text="Use /setbanner to equip your new banner!")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"You need {banner_data['price']} PuroCoins to buy this banner!", ephemeral=True)

@bot.tree.command(name="setbanner", description="Set your profile banner!")
async def set_banner(interaction: discord.Interaction, banner: str):
    profile = get_user_profile(interaction.user.id)
    banner_id = banner.lower().replace(" ", "_")
    
    if banner_id not in BANNERS:
        await interaction.response.send_message("*Puro looks confused* That banner doesn't exist!", ephemeral=True)
        return
    
    if profile.set_banner(banner_id):
        embed = discord.Embed(
            title="Banner Updated!",
            description=f"Your profile banner is now set to **{BANNERS[banner_id]['name']}**!",
            color=0x00FF00
        )
        embed.set_image(url=BANNERS[banner_id]["url"])
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You don't own this banner yet! Use `/buybanner` to purchase it.", ephemeral=True)

@set_banner.autocomplete('banner')
async def banner_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    profile = get_user_profile(interaction.user.id)
    banners = []
    for banner_id, banner in BANNERS.items():
        name = f"{banner['name']} - {banner['description']}"
        if banner_id not in profile.owned_banners:
            name += " (🔒 Not Owned)"
        if current.lower() in name.lower():
            banners.append(app_commands.Choice(name=name, value=banner_id))
    return banners[:25]

@bot.tree.command(name="daily", description="Claim your daily reward!")
async def daily_reward(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    if not profile.can_claim_daily():
        # Calculate time until next claim
        now = datetime.datetime.now()
        last_claim = datetime.datetime.fromtimestamp(profile.last_daily)
        next_claim = last_claim + datetime.timedelta(hours=20)
        time_left = next_claim - now
        hours = int(time_left.total_seconds() / 3600)
        minutes = int((time_left.total_seconds() % 3600) / 60)
        
        embed = discord.Embed(
            title="Daily Reward Not Ready",
            description=f"*Puro is still preparing your next reward!*\nCome back in **{hours}h {minutes}m**",
            color=0xFF0000
        )
        embed.set_footer(text="Daily rewards reset every 20 hours!")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    rewards = profile.claim_daily()
    
    embed = discord.Embed(
        title="🎁 Daily Reward Claimed!",
        description=f"**{rewards['description']}**\n\nYou received:\n{COIN_EMOJI} {rewards['coins']} PuroCoins\n✨ {rewards['xp']} XP",
        color=0x00FF00
    )
    
    # Show streak information
    streak_bar = f"{FILLED_STREAK_EMOJI} " * profile.daily_streak + f"{STREAK_EMOJI} " * (7 - profile.daily_streak)
    embed.add_field(
        name="Daily Streak",
        value=f"Day {profile.daily_streak} of 7\n{streak_bar}",
        inline=False
    )
    
    # Show next day's reward
    if profile.daily_streak < 7:
        next_rewards = DAILY_REWARDS[profile.daily_streak + 1]
        embed.add_field(
            name="Next Day's Reward",
            value=f"{COIN_EMOJI} {next_rewards['coins']} PuroCoins\n✨ {next_rewards['xp']} XP",
            inline=False
        )
    
    embed.set_footer(text="Come back in 20 hours for your next reward!")
    embed.set_author(name="Daily Rewards", icon_url=bot.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="achievements", description="View your achievements!")
async def view_achievements(interaction: discord.Interaction):
    profile = get_user_profile(interaction.user.id)
    
    # Check for new achievements
    new_achievements = profile.check_achievements()
    
    embed = discord.Embed(
        title="🏆 Achievements",
        description="Track your progress and earn rewards!",
        color=0x000000
    )
    
    # Group achievements by category
    completed = []
    in_progress = []
    secret = []
    
    for ach_id, ach in ACHIEVEMENTS.items():
        if ach["secret"] and ach_id not in profile.achievements:
            secret.append("🔒 ???")
            continue
            
        status = "✅" if ach_id in profile.achievements else "❌"
        text = f"{ach['emoji']} **{ach['name']}**\n*{ach['description']}*\nRewards: {COIN_EMOJI} {ach['reward_coins']} PuroCoins, ✨ {ach['reward_xp']} XP"
        
        if ach_id in profile.achievements:
            completed.append(f"{status} {text}")
        else:
            in_progress.append(f"{status} {text}")
    
    if completed:
        embed.add_field(
            name="Completed Achievements",
            value="\n\n".join(completed),
            inline=False
        )
    
    if in_progress:
        embed.add_field(
            name="Available Achievements",
            value="\n\n".join(in_progress),
            inline=False
        )
    
    if secret:
        embed.add_field(
            name="Secret Achievements",
            value="\n".join(secret),
            inline=False
        )
    
    embed.set_footer(text=f"Completed: {len(profile.achievements)}/{len(ACHIEVEMENTS)}")
    
    await interaction.response.send_message(embed=embed)
    
    # Show new achievements if any were earned
    if new_achievements:
        for achievement in new_achievements:
            reward_embed = discord.Embed(
                title="🎉 Achievement Unlocked!",
                description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                color=0x00FF00
            )
            reward_embed.add_field(
                name="Rewards",
                value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                inline=False
            )
            await interaction.channel.send(embed=reward_embed)

@bot.tree.command(name="setguessinterval", description="Set how often the guess number game should run")
@commands.has_permissions(administrator=True)
async def set_guess_interval(interaction: discord.Interaction, value: int, unit: str):
    """Set the interval for the guess number game
    Parameters:
    value: The number of time units
    unit: minutes/hours/days
    """
    unit = unit.lower()
    if unit not in ['minutes', 'hours', 'days', 'minute', 'hour', 'day']:
        await interaction.response.send_message("Please use 'minutes', 'hours', or 'days' as the time unit!", ephemeral=True)
        return
    
    # Convert everything to minutes
    if unit.startswith('hour'):
        minutes = value * 60
    elif unit.startswith('day'):
        minutes = value * 24 * 60
    else:
        minutes = value
    
    # Minimum 5 minutes, maximum 7 days
    if minutes < 5:
        await interaction.response.send_message("The interval cannot be less than 5 minutes!", ephemeral=True)
        return
    if minutes > 10080:  # 7 days in minutes
        await interaction.response.send_message("The interval cannot be more than 7 days!", ephemeral=True)
        return
    
    # Update the configuration
    GUESS_GAME_CONFIG["interval_minutes"] = minutes
    
    # Restart the task with new interval if it's running
    if guess_number_game.is_running():
        guess_number_game.cancel()
        guess_number_game.change_interval(minutes=minutes)
        guess_number_game.start()
    
    # Format time for display
    if minutes < 60:
        time_str = f"{minutes} minutes"
    elif minutes < 1440:
        hours = minutes // 60
        time_str = f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = minutes // 1440
        time_str = f"{days} day{'s' if days != 1 else ''}"
    
    embed = discord.Embed(
        title="⚙️ Guess Game Interval Updated",
        description=f"The guess number game will now run every **{time_str}**!",
        color=0x00FF00
    )
    embed.set_footer(text="Use /setguesschannel to start the game in a channel")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="setguesschannel", description="Set the channel for the automated guess number game")
@commands.has_permissions(administrator=True)
async def set_guess_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    GUESS_GAME_CONFIG["channel_id"] = channel.id
    await interaction.response.send_message(f"Guess the number game channel set to {channel.mention}!")
    if not guess_number_game.is_running():
        guess_number_game.start()

@tasks.loop(minutes=20)  # Default interval, will be changed by setguessinterval
async def guess_number_game():
    if GUESS_GAME_CONFIG["channel_id"] is None:
        return
        
    channel = bot.get_channel(GUESS_GAME_CONFIG["channel_id"])
    if channel is None:
        return

    # End previous game if it exists
    if GUESS_GAME_CONFIG["active_game"]:
        await channel.send(f"Previous game ended! The number was {GUESS_GAME_CONFIG['current_number']}.")
        if not GUESS_GAME_CONFIG["winners"]:
            await channel.send("No one guessed the number correctly!")
    
    # Start new game
    GUESS_GAME_CONFIG["current_number"] = random.randint(GUESS_GAME_CONFIG["min_number"], GUESS_GAME_CONFIG["max_number"])
    GUESS_GAME_CONFIG["active_game"] = True
    GUESS_GAME_CONFIG["winners"].clear()
    GUESS_GAME_CONFIG["last_game_time"] = datetime.datetime.now()
    
    # Calculate when the next game will be
    next_game = datetime.datetime.now() + datetime.timedelta(minutes=GUESS_GAME_CONFIG["interval_minutes"])
    
    embed = discord.Embed(
        title="🎲 Guess the Number!",
        description=f"I'm thinking of a number between {GUESS_GAME_CONFIG['min_number']} and {GUESS_GAME_CONFIG['max_number']}!\nType your guess in the chat!",
        color=0x00FF00
    )
    
    # Format next game time
    if GUESS_GAME_CONFIG["interval_minutes"] < 60:
        time_str = f"{GUESS_GAME_CONFIG['interval_minutes']} minutes"
    elif GUESS_GAME_CONFIG["interval_minutes"] < 1440:
        hours = GUESS_GAME_CONFIG["interval_minutes"] // 60
        time_str = f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = GUESS_GAME_CONFIG["interval_minutes"] // 1440
        time_str = f"{days} day{'s' if days != 1 else ''}"
    
    embed.set_footer(text=f"Game will end in {time_str}!")
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)
    
    # Check if message is in guess game channel and game is active
    if (GUESS_GAME_CONFIG["channel_id"] == message.channel.id and 
        GUESS_GAME_CONFIG["active_game"] and 
        message.author.id not in GUESS_GAME_CONFIG["winners"]):
        
        try:
            guess = int(message.content)
            if guess == GUESS_GAME_CONFIG["current_number"]:
                GUESS_GAME_CONFIG["winners"].add(message.author.id)
                profile = get_user_profile(message.author.id)
                reward_coins = 50
                reward_xp = 25
                
                profile.puro_coins += reward_coins  # Directly add coins
                profile.add_xp(reward_xp)  # Use existing add_xp method
                profile.guess_wins += 1  # Increment guess wins
                
                # Check achievements after winning
                new_achievements = profile.check_achievements()
                
                embed = discord.Embed(
                    title="🎉 Correct Guess!",
                    description=f"Congratulations {message.author.mention}! You guessed the number!\n\nRewards:\n{COIN_EMOJI} {reward_coins} PuroCoins\n✨ {reward_xp} XP",
                    color=0x00FF00
                )
                await message.channel.send(embed=embed)
                
                # Show any new achievements
                if new_achievements:
                    for achievement in new_achievements:
                        reward_embed = discord.Embed(
                            title="🎉 Achievement Unlocked!",
                            description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                            color=0x00FF00
                        )
                        reward_embed.add_field(
                            name="Rewards",
                            value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                            inline=False
                        )
                        await message.channel.send(embed=reward_embed)
            elif guess < GUESS_GAME_CONFIG["current_number"]:
                embed = discord.Embed(
                    description=f"*Puro shakes his head* {message.author.mention}, your guess is **too low**! Try a higher number!",
                    color=0xFF5555
                )
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"*Puro shakes his head* {message.author.mention}, your guess is **too high**! Try a lower number!",
                    color=0xFF5555
                )
                await message.channel.send(embed=embed)
        except ValueError:
            pass  # Not a number, ignore

@bot.tree.command(name="stopguess", description="Stop the automated guess number game")
@commands.has_permissions(administrator=True)
async def stop_guess_game(interaction: discord.Interaction):
    if guess_number_game.is_running():
        guess_number_game.cancel()
        GUESS_GAME_CONFIG["channel_id"] = None
        GUESS_GAME_CONFIG["active_game"] = False
        await interaction.response.send_message("Automated guess number game has been stopped!")
    else:
        await interaction.response.send_message("The game is not currently running!")

@bot.tree.command(name="clean", description="Clean messages from the channel (Staff only)")
@commands.has_permissions(manage_messages=True)
async def clean_messages(interaction: discord.Interaction, amount: int):
    """Clean messages from the channel
    Parameters:
    amount: Number of messages to delete (max 50)
    """
    if amount < 1:
        await interaction.response.send_message("*Puro tilts his head* Please specify at least 1 message to clean!", ephemeral=True)
        return
    
    if amount > 50:
        await interaction.response.send_message("*Puro looks worried* I can only clean up to 50 messages at once!", ephemeral=True)
        return
    
    # Defer the response since deletion might take a moment
    await interaction.response.defer(ephemeral=True)
    
    # Delete messages
    deleted = await interaction.channel.purge(limit=amount)
    
    # Random success messages with Puro's style
    success_messages = [
        "*Puro wipes the chat clean with his paws* All done! 🐾",
        "*Puro uses his special latex powers to clean the chat* Nice and tidy! 🧹",
        "*Puro carefully removes the messages* The chat is now spotless! 🌟",
        "*Puro helps organize the chat* Everything's clean now! ✨",
        "*Puro proudly shows off his cleaning work* All cleaned up! 🧼"
    ]
    
    # Send confirmation
    embed = discord.Embed(
        title="🧹 Chat Cleaned!",
        description=f"{random.choice(success_messages)}\n\nRemoved **{len(deleted)}** messages.",
        color=0x00FF00
    )
    embed.set_footer(text="Keeping things tidy for everyone!")
    
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="setlevel", description="Set a user's level (Requires Puro role)")
async def set_level(interaction: discord.Interaction, user: discord.Member, level: int):
    if not discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        await interaction.response.send_message("*Puro looks at you confused* Only my special friend can use this command!", ephemeral=True)
        return
        
    if level < 1 or level > 100:
        await interaction.response.send_message("Please choose a level between 1 and 100!", ephemeral=True)
        return
        
    profile = get_user_profile(user.id)
    profile.level = level
    profile.xp = 0  # Reset XP for new level
    
    embed = discord.Embed(
        title="Level Updated!",
        description=f"Set {user.mention}'s level to **{level}**!",
        color=0x00FF00
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="setcoins", description="Set a user's PuroCoins (Requires Puro role)")
async def set_coins(interaction: discord.Interaction, user: discord.Member, amount: int):
    if not discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        await interaction.response.send_message("*Puro looks at you confused* Only my special friend can use this command!", ephemeral=True)
        return
        
    if amount < 0:
        await interaction.response.send_message("Amount cannot be negative!", ephemeral=True)
        return
        
    profile = get_user_profile(user.id)
    profile.puro_coins = amount
    
    embed = discord.Embed(
        title="PuroCoins Updated!",
        description=f"Set {user.mention}'s PuroCoins to **{amount}** {COIN_EMOJI}!",
        color=0x00FF00
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unlockall", description="Unlock all items and banners for a user (Requires Puro role)")
async def unlock_all(interaction: discord.Interaction, user: discord.Member):
    if not discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        await interaction.response.send_message("*Puro looks at you confused* Only my special friend can use this command!", ephemeral=True)
        return
        
    profile = get_user_profile(user.id)
    
    # Unlock all shop items
    for item_id in SHOP_ITEMS:
        if item_id not in profile.inventory:
            profile.add_item(item_id)
    
    # Unlock all banners
    for banner_id in BANNERS:
        profile.owned_banners.add(banner_id)
    
    embed = discord.Embed(
        title="🎉 Everything Unlocked!",
        description=f"Unlocked all items and banners for {user.mention}!",
        color=0x00FF00
    )
    embed.add_field(name="Items Unlocked", value=f"✨ {len(SHOP_ITEMS)} items", inline=True)
    embed.add_field(name="Banners Unlocked", value=f"🎨 {len(BANNERS)} banners", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unlockachievements", description="Unlock all achievements for a user (Requires Puro role)")
async def unlock_achievements(interaction: discord.Interaction, user: discord.Member):
    if not discord.utils.get(interaction.user.roles, name=OWNER_ROLE_NAME):
        await interaction.response.send_message("*Puro looks at you confused* Only my special friend can use this command!", ephemeral=True)
        return
        
    profile = get_user_profile(user.id)
    
    # Unlock all achievements
    for achievement_id in ACHIEVEMENTS:
        if achievement_id not in profile.achievements:
            achievement = profile.earn_achievement(achievement_id)
            if achievement:
                embed = discord.Embed(
                    title="🎉 Achievement Unlocked!",
                    description=f"{achievement['emoji']} **{achievement['name']}**\n*{achievement['description']}*",
                    color=0x00FF00
                )
                embed.add_field(
                    name="Rewards",
                    value=f"{COIN_EMOJI} {achievement['reward_coins']} PuroCoins\n✨ {achievement['reward_xp']} XP",
                    inline=False
                )
                await interaction.channel.send(embed=embed)
    
    summary_embed = discord.Embed(
        title="🏆 All Achievements Unlocked!",
        description=f"Unlocked all achievements for {user.mention}!",
        color=0x00FF00
    )
    summary_embed.add_field(
        name="Total Achievements",
        value=f"✨ {len(ACHIEVEMENTS)} achievements unlocked",
        inline=False
    )
    
    await interaction.response.send_message(embed=summary_embed)

class Giveaway:
    def __init__(self, message_id, channel_id, prize, winners, end_time, host_id, required_role=None, dm_message=None, unique_prizes=None):
        self.message_id = message_id
        self.channel_id = channel_id
        self.prize = prize
        self.winners_count = winners
        self.end_time = end_time
        self.host_id = host_id
        self.required_role = required_role
        self.dm_message = dm_message
        self.participants = set()
        self.unique_prizes = unique_prizes or []  # List of individual prizes/keys

    def add_participant(self, user_id):
        self.participants.add(user_id)

    def remove_participant(self, user_id):
        self.participants.discard(user_id)

    def get_winners(self):
        eligible = list(self.participants)
        if not eligible:
            return []
        return random.sample(eligible, min(self.winners_count, len(eligible)))

    def time_remaining(self):
        now = datetime.datetime.now()
        end = datetime.datetime.fromtimestamp(self.end_time)
        remaining = end - now
        
        if remaining.total_seconds() <= 0:
            return "Ended"
            
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        seconds = remaining.seconds % 60
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0:
            parts.append(f"{seconds}s")
            
        return " ".join(parts)

@bot.tree.command(name="giveaway", description="Start a new giveaway!")
@commands.has_permissions(administrator=True)
async def create_giveaway(
    interaction: discord.Interaction, 
    prize: str,
    winners: int,
    duration: str,
    required_role: discord.Role = None,
    dm_message: str = None
):
    """Create a new giveaway
    Parameters:
    prize: What to give away
    winners: Number of winners
    duration: Duration (e.g. 1h, 2d, 1w)
    required_role: Role required to enter (optional)
    dm_message: Custom message to send to winners (optional)
    """
    # First, let's collect the unique prizes if this is a key giveaway
    unique_prizes = []
    if "key" in prize.lower() or "code" in prize.lower():
        modal_msg = await interaction.response.send_message(
            "Please send each game key in separate messages. Send 'done' when finished.", 
            ephemeral=True
        )
        
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            while True:
                msg = await bot.wait_for('message', timeout=300.0, check=check)
                if msg.content.lower() == 'done':
                    break
                unique_prizes.append(msg.content)
                try:
                    await msg.delete()  # Delete the message containing the key
                except:
                    pass
                await interaction.followup.send(
                    f"Key {len(unique_prizes)} added! Send next key or 'done' to finish.", 
                    ephemeral=True
                )
        except TimeoutError:
            await interaction.followup.send("Giveaway creation timed out!", ephemeral=True)
            return
        
        # Validate number of winners matches number of keys
        if len(unique_prizes) != winners:
            await interaction.followup.send(
                f"Number of winners ({winners}) must match number of keys provided ({len(unique_prizes)})!", 
                ephemeral=True
            )
            return
    
    # Validate winners count
    if winners < 1:
        await interaction.followup.send("You must have at least 1 winner!", ephemeral=True)
        return
        
    # Parse duration
    duration_regex = re.compile(r"(\d+)([smhdw])")
    match = duration_regex.match(duration.lower())
    if not match:
        await interaction.followup.send(
            "Invalid duration format! Use a number followed by s/m/h/d/w (e.g. 30s, 5m, 2h, 1d, 1w)",
            ephemeral=True
        )
        return
        
    amount = int(match.group(1))
    unit = match.group(2)
    
    # Convert to seconds
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
    total_seconds = amount * multipliers[unit]
    
    # Check maximum duration (30 days)
    if total_seconds > 2592000:  # 30 days in seconds
        await interaction.followup.send("Giveaway duration cannot exceed 30 days!", ephemeral=True)
        return
        
    # Calculate end time
    end_time = datetime.datetime.now().timestamp() + total_seconds
    
    # Create embed
    embed = discord.Embed(
        title="🎉 New Giveaway! 🎉",
        description=f"# {prize}\n\n"
                   f"React with {GIVEAWAY_EMOJI} to enter!\n\n"
                   f"**Winners:** {winners}\n"
                   f"**Hosted by:** {interaction.user.mention}\n"
                   f"**Required Role:** {required_role.mention if required_role else 'None'}\n\n"
                   f"Ends in: **{duration}**",
        color=0x2b2d31
    )
    
    embed.set_footer(text="Good luck everyone! 🍀")
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_image(url=GIVEAWAY_PURO_GIF)
    
    # Send giveaway message
    if not unique_prizes:  # If we haven't sent an initial response yet
        await interaction.response.send_message("Creating giveaway...", ephemeral=True)
    giveaway_msg = await interaction.channel.send(embed=embed)
    await giveaway_msg.add_reaction(GIVEAWAY_EMOJI)
    
    # Store giveaway data
    GIVEAWAY_CONFIG["active_giveaways"][giveaway_msg.id] = Giveaway(
        giveaway_msg.id,
        interaction.channel.id,
        prize,
        winners,
        end_time,
        interaction.user.id,
        required_role,
        dm_message,
        unique_prizes
    )
    
    # Start checking task if not running
    if not check_giveaways.is_running():
        check_giveaways.start()

@tasks.loop(seconds=5)
async def check_giveaways():
    current_time = datetime.datetime.now().timestamp()
    
    for giveaway_id, giveaway in list(GIVEAWAY_CONFIG["active_giveaways"].items()):
        if current_time >= giveaway.end_time and giveaway_id not in GIVEAWAY_CONFIG["ended_giveaways"]:
            # Mark as ended
            GIVEAWAY_CONFIG["ended_giveaways"].add(giveaway_id)
            
            try:
                channel = bot.get_channel(giveaway.channel_id)
                if not channel:
                    continue
                    
                message = await channel.fetch_message(giveaway_id)
                if not message:
                    continue
                
                # Get winners
                winners = giveaway.get_winners()
                
                # Update embed
                embed = message.embeds[0]
                
                if winners:
                    winner_mentions = [f"<@{winner_id}>" for winner_id in winners]
                    winners_text = ", ".join(winner_mentions)
                    
                    embed.description = f"# {giveaway.prize}\n\n"
                    embed.description += f"🎉 **Winners:** {winners_text}\n\n"
                    embed.description += f"**Hosted by:** <@{giveaway.host_id}>"
                    
                    # Send DM to winners
                    for i, winner_id in enumerate(winners):
                        try:
                            winner = await bot.fetch_user(winner_id)
                            if winner:
                                win_embed = discord.Embed(
                                    title="🎉 Congratulations! You Won!",
                                    description=f"You won the giveaway for:\n# {giveaway.prize}",
                                    color=0x00FF00
                                )
                                
                                # Add the unique prize if available
                                if giveaway.unique_prizes and i < len(giveaway.unique_prizes):
                                    win_embed.add_field(
                                        name="Your Game Key:",
                                        value=f"```{giveaway.unique_prizes[i]}```",
                                        inline=False
                                    )
                                
                                if giveaway.dm_message:
                                    win_embed.add_field(
                                        name="Message from the host:",
                                        value=giveaway.dm_message,
                                        inline=False
                                    )
                                    
                                win_embed.set_footer(text="Thank you for participating! 🎊")
                                win_embed.set_image(url=GIVEAWAY_PURO_GIF)
                                
                                await winner.send(embed=win_embed)
                        except:
                            continue
                else:
                    embed.description = f"# {giveaway.prize}\n\n"
                    embed.description += "No valid winners! 😢\n\n"
                    embed.description += f"**Hosted by:** <@{giveaway.host_id}>"
                
                embed.color = 0x2b2d31
                embed.set_footer(text="Giveaway Ended 🎊")
                
                await message.edit(embed=embed)
                
                # Send announcement message
                announce_embed = discord.Embed(
                    title="🎉 Giveaway Ended!",
                    description=f"**Prize:** {giveaway.prize}\n\n" + 
                              ("**Winners:** " + winners_text if winners else "No valid winners! 😢"),
                    color=0x00FF00
                )
                announce_embed.set_footer(text="Congratulations to the winners! 🎊")
                await channel.send(embed=announce_embed)
                
            except Exception as e:
                print(f"Error ending giveaway {giveaway_id}: {e}")
                continue
            
            # Remove from active giveaways
            GIVEAWAY_CONFIG["active_giveaways"].pop(giveaway_id, None)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
        
    if payload.message_id in GIVEAWAY_CONFIG["active_giveaways"]:
        giveaway = GIVEAWAY_CONFIG["active_giveaways"][payload.message_id]
        
        if str(payload.emoji) == GIVEAWAY_EMOJI:
            # Check role requirement
            if giveaway.required_role:
                member = payload.member
                if not member or not discord.utils.get(member.roles, id=giveaway.required_role.id):
                    try:
                        channel = bot.get_channel(payload.channel_id)
                        message = await channel.fetch_message(payload.message_id)
                        await message.remove_reaction(payload.emoji, payload.member)
                        
                        await payload.member.send(
                            f"You need the {giveaway.required_role.name} role to enter this giveaway!"
                        )
                    except:
                        pass
                    return
            
            giveaway.add_participant(payload.user_id)

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in GIVEAWAY_CONFIG["active_giveaways"]:
        if str(payload.emoji) == GIVEAWAY_EMOJI:
            giveaway = GIVEAWAY_CONFIG["active_giveaways"][payload.message_id]
            giveaway.remove_participant(payload.user_id)

@bot.tree.command(name="reroll", description="Reroll a giveaway winner")
@commands.has_permissions(administrator=True)
async def reroll_giveaway(interaction: discord.Interaction, message_id: str):
    """Reroll a giveaway winner
    Parameters:
    message_id: The ID of the giveaway message
    """
    try:
        message_id = int(message_id)
        if message_id not in GIVEAWAY_CONFIG["ended_giveaways"]:
            await interaction.response.send_message("That's not a valid ended giveaway!", ephemeral=True)
            return
            
        channel = interaction.channel
        message = await channel.fetch_message(message_id)
        
        if not message or not message.embeds:
            await interaction.response.send_message("Couldn't find the giveaway message!", ephemeral=True)
            return
            
        # Get original giveaway data from embed
        embed = message.embeds[0]
        prize = embed.description.split("\n")[0].strip("# ")
        
        # Get reactions
        reaction = discord.utils.get(message.reactions, emoji=GIVEAWAY_EMOJI)
        if not reaction:
            await interaction.response.send_message("No participants found!", ephemeral=True)
            return
            
        users = [user.id async for user in reaction.users() if user.id != bot.user.id]
        if not users:
            await interaction.response.send_message("No valid participants found!", ephemeral=True)
            return
            
        # Pick new winner
        winner_id = random.choice(users)
        winner = await bot.fetch_user(winner_id)
        
        # Announce new winner
        reroll_embed = discord.Embed(
            title="🎉 Giveaway Rerolled!",
            description=f"**Prize:** {prize}\n**New Winner:** {winner.mention}",
            color=0x00FF00
        )
        reroll_embed.set_footer(text="Congratulations to the new winner! 🎊")
        
        await interaction.response.send_message(embed=reroll_embed)
        
        # DM the new winner
        try:
            win_embed = discord.Embed(
                title="🎉 Congratulations! You Won!",
                description=f"You won the reroll for:\n# {prize}",
                color=0x00FF00
            )
            win_embed.set_footer(text="Thank you for participating! 🎊")
            win_embed.set_image(url=GIVEAWAY_PURO_GIF)
            
            await winner.send(embed=win_embed)
        except:
            pass
            
    except ValueError:
        await interaction.response.send_message("Please provide a valid message ID!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
