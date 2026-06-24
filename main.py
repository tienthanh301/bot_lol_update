import discord
from discord.ext import commands, tasks
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_version = "test_version"


def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    res = requests.get(url)
    data = res.json()
    return data[0]  # version mới nhất


def create_embed(version):
    embed = discord.Embed(
        title=f"🔥 New LoL Update: {version}",
        description=f"Phiên bản mới đã ra mắt!",
        color=0x00ff00
    )

    # ảnh splash đại diện
    splash = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg"

    embed.set_image(url=splash)
    embed.add_field(
        name="Patch Notes",
        value=f"https://www.leagueoflegends.com/en-us/news/tags/patch-notes/",
        inline=False
    )

    return embed


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    check_update.start()


@tasks.loop(minutes=5)
async def check_update():
    global last_version

    try:
        version = get_latest_version()

        if last_version is None:
            last_version = version
            return

        if version != last_version:
            last_version = version

            channel = bot.get_channel(CHANNEL_ID)

            if channel:
                embed = create_embed(version)
                await channel.send(embed=embed)

                print("Đã gửi update:", version)

    except Exception as e:
        print("Lỗi:", e)


bot.run(TOKEN)