import discord
from discord.ext import commands, tasks
import requests
import feedparser

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = 123456789012345678  # ID kênh bạn muốn bot gửi

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

latest_link = None


# ================= FETCH PATCH =================
def get_latest_patch():
    url = "https://www.leagueoflegends.com/en-us/rss.xml"
    feed = feedparser.parse(url)

    for entry in feed.entries:
        if "Patch" in entry.title:
            title = entry.title
            link = entry.link

            # Lấy ảnh từ nội dung
            image = None
            if "media_content" in entry:
                image = entry.media_content[0]['url']
            elif "summary" in entry:
                import re
                match = re.search(r'<img src="(.*?)"', entry.summary)
                if match:
                    image = match.group(1)

            return title, link, image

    return None, None, None


# ================= BOT READY =================
@bot.event
async def on_ready():
    print(f"Bot đã online: {bot.user}")
    check_update.start()


# ================= AUTO CHECK =================
@tasks.loop(minutes=10)
async def check_update():
    global latest_link

    channel = bot.get_channel(CHANNEL_ID)

    title, link, image = get_latest_patch()

    if not link:
        print("Không lấy được patch")
        return

    if link != latest_link:
        latest_link = link

        embed = discord.Embed(
            title=title,
            url=link,
            description="🔔 Patch mới từ Riot!",
            color=0x00ff00
        )

        if image:
            embed.set_image(url=image)

        await channel.send(embed=embed)
        print("Đã gửi patch mới!")


# ================= TEST COMMAND =================
@bot.command()
async def test(ctx):
    title, link, image = get_latest_patch()

    if not link:
        await ctx.send("❌ Không lấy được dữ liệu patch!")
        return

    embed = discord.Embed(
        title=title,
        url=link,
        description="🧪 Test patch",
        color=0xff0000
    )

    if image:
        embed.set_image(url=image)

    await ctx.send(embed=embed)


bot.run(TOKEN)