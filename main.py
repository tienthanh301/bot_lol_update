import discord
import os
import requests
from discord.ext import tasks, commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

sent_patches = set()

# 🔥 Lấy dữ liệu patch từ Riot
def get_patches():
    url = "https://www.leagueoflegends.com/en-us/news/tags/patch-notes/"
    response = requests.get(url)
    
    # ⚠️ Riot không có API chính thức → ta fake demo data
    # Bạn có thể nâng cấp sau bằng RSS
    
    return [
        {
            "title": "Patch 14.10 Notes",
            "link": "https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-10-notes/",
            "image": "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt_patch.jpg"
        },
        {
            "title": "Patch 14.9 Notes",
            "link": "https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-9-notes/",
            "image": "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt_patch.jpg"
        },
        {
            "title": "Patch 14.8 Notes",
            "link": "https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-8-notes/",
            "image": "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt_patch.jpg"
        }
    ]

# 📤 Gửi embed đẹp
async def send_patch(channel, patch):
    embed = discord.Embed(
        title=patch["title"],
        url=patch["link"],
        description="🔥 Riot vừa cập nhật patch mới!",
        color=0x00ff00
    )
    embed.set_image(url=patch["image"])
    
    await channel.send(embed=embed)

# ✅ Khi bot online
@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    
    channel = bot.get_channel(CHANNEL_ID)
    
    patches = get_patches()
    
    # 🔥 Gửi 3 patch gần nhất
    for patch in patches:
        if patch["title"] not in sent_patches:
            await send_patch(channel, patch)
            sent_patches.add(patch["title"])
    
    check_updates.start()

# 🔁 Auto check mỗi 1 giờ
@tasks.loop(minutes=60)
async def check_updates():
    channel = bot.get_channel(CHANNEL_ID)
    patches = get_patches()
    
    for patch in patches:
        if patch["title"] not in sent_patches:
            await send_patch(channel, patch)
            sent_patches.add(patch["title"])

bot.run(TOKEN)