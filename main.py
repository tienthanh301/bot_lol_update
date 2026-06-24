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

    while not client.is_closed():
        try:
            feed = feedparser.parse(RSS_URL)

            if feed.entries:
                latest = feed.entries[0]
                title = latest.title
                link = latest.link

                if last_link is None:
                    last_link = link

                elif link != last_link:
                    last_link = link

                    embed = discord.Embed(
                        title="🚨 LoL Update mới!",
                        description=f"**{title}**\n{link}",
                        color=0x00ff00
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