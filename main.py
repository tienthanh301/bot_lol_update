import discord
import feedparser
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

RSS_URL = "https://www.leagueoflegends.com/en-us/rss.xml"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_link = None


async def check_updates():
    global last_link

    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # 🚀 Gửi 3 bản cập nhật gần nhất khi bot khởi động
    try:
        feed = feedparser.parse(RSS_URL)

        if feed.entries:
            top3 = feed.entries[:3]

            await channel.send("📢 **3 bản cập nhật LoL gần nhất:**")

            for entry in top3:
                embed = discord.Embed(
                    title=entry.title,
                    url=entry.link,
                    description="🔔 Cập nhật từ Riot Games",
                    color=0x00ff00
                )
                await channel.send(embed=embed)

            # lưu bản mới nhất để tránh gửi lại
            last_link = top3[0].link

    except Exception as e:
        print("Lỗi khi lấy top 3:", e)

    # 🔁 Loop check update mới
    while not client.is_closed():
        try:
            feed = feedparser.parse(RSS_URL)

            if feed.entries:
                latest = feed.entries[0]

                if latest.link != last_link:
                    last_link = latest.link

                    embed = discord.Embed(
                        title="🚨 LoL Update mới!",
                        description=f"**{latest.title}**\n{latest.link}",
                        color=0xff0000
                    )

                    await channel.send(embed=embed)

        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"Bot chạy với {client.user}")
    client.loop.create_task(check_updates())


client.run(TOKEN)