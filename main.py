import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_patch = None


def get_latest_patch():
    url = "https://www.leagueoflegends.com/en-us/news/tags/patch-notes/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.find_all("a", href=True)

    for a in articles:
        link = a["href"]

        if "patch" in link and "notes" in link:
            title = a.text.strip()

            if "Patch" in title:
                full_link = "https://www.leagueoflegends.com" + link

                # lấy version
                import re
                match = re.search(r"(\d+\.\d+)", title)
                version = match.group(1) if match else "Unknown"

                # 🔥 LẤY ẢNH TỪ BÀI PATCH
                image = get_patch_image(full_link)

                return {
                    "title": title,
                    "version": version,
                    "link": full_link,
                    "image": image
                }

    return None


def get_patch_image(patch_url):
    try:
        res = requests.get(patch_url)
        soup = BeautifulSoup(res.text, "html.parser")

        img = soup.find("img")

        if img and img.get("src"):
            return img["src"]

    except:
        pass

    # fallback nếu lỗi
    return "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/default.jpg"


def create_embed(patch):
    embed = discord.Embed(
        title=f"🔥 {patch['title']}",
        url=patch["link"],
        description=f"📢 Patch {patch['version']} đã ra!",
        color=0x00ff00
    )

    # ảnh lớn hơn
    embed.set_image(url=patch["image"])

    embed.add_field(
        name="👉 Xem chi tiết",
        value=patch["link"],
        inline=False
    )

    return embed


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    check_update.start()


@tasks.loop(minutes=5)
async def check_update():
    global last_patch

    try:
        patch = get_latest_patch()

        if not patch:
            return

        if last_patch is None:
            last_patch = patch["version"]
            return

        if patch["version"] != last_patch:
            last_patch = patch["version"]

            channel = bot.get_channel(CHANNEL_ID)

            if channel:
                embed = create_embed(patch)
                await channel.send(embed=embed)

                print("Đã gửi patch:", patch["version"])

    except Exception as e:
        print("Lỗi:", e)


# 🧪 TEST COMMAND
@bot.command()
async def test(ctx):
    patch = get_latest_patch()

    if patch:
        embed = create_embed(patch)
        await ctx.send("✅ Test OK", embed=embed)
    else:
        await ctx.send("❌ Không lấy được patch")


bot.run(TOKEN)