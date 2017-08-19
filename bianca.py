import discord
import asyncio
import json
import datetime
import pytz
import feedparser

client = discord.Client()

with open('reminders.json', encoding='utf-8') as data_file:
    reminders = json.load(data_file)

with open('rss.json', encoding='utf-8') as data_file:
    rss = json.load(data_file)

with open('config.json', encoding='utf-8') as config_file:
    config = json.load(config_file)
tz = pytz.timezone(config["timezone"])

async def check():
    await client.wait_until_ready()
    channel = discord.Object(id=config["channel_id"])
    while not client.is_closed:
        print("Running at " + datetime.datetime.now(tz).strftime("%c"))
        await check_feeds(channel)
        await check_events(channel)
        await asyncio.sleep(config["refresh_interval"])

async def check_events(channel):
    for event in reminders["events"]:
        if is_current(event["at"]):
            await client.send_message(channel, event["message"])

async def check_feeds(channel):
    with open("rss-seen.txt") as f:
        known_items = f.readlines()
    known_items = [x.strip() for x in known_items]
    message_names = []
    message_queue = []
    for feed in rss["rss_feeds"]:
        feed_data = feedparser.parse(feed["url"])
        for item in feed_data["entries"]:
            if feed["name"] + "-" + item["post-id"] not in known_items:
                message_names.append(feed["name"] + "-" + item["post-id"])
                message_queue.append(feed["message"].replace("{author}",item["author"]).replace("{url}",item["link"]).replace("{title}",item["title"]))
    for name in message_names:
        with open("rss-seen.txt","a+") as f:
            f.write(name + "\n")
    for message in message_queue:
        await client.send_message(channel, message)

@client.event
async def on_ready():
    print("BIANCA DISCORD BOT - https://github.com/Nanofus/bianca")
    print("\nLogged in as")
    print(client.user.name)
    print(client.user.id)
    print("\n------\n")

def is_current(event_time):
    times = event_time.split(" ")
    for time in times:
        if time.split("-")[0] == "YEAR" and time.split("-")[1] != datetime.datetime.now(tz).strftime("%Y"):
            return False
        if time.split("-")[0] == "MONTH" and time.split("-")[1] != datetime.datetime.now(tz).strftime("%m"):
            return False
        if time.split("-")[0] == "DAY" and time.split("-")[1] != datetime.datetime.now(tz).strftime("%d"):
            return False
        if time.split("-")[0] == "WKD" and time.split("-")[1] != datetime.datetime.now(tz).strftime("%a"):
            return False
        if time.split("-")[0] == "TIME" and time.split("-")[1] != datetime.datetime.now(tz).strftime("%H:%M"):
            return False
    return True

client.loop.create_task(check())
client.run(config["client_token"])
