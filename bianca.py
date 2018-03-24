# Load dependencies
import discord
import asyncio
import json
import datetime
import pytz
import feedparser

# Load reminders
with open("reminders.json", encoding="utf-8") as data_file:
    reminders = json.load(data_file)

# Load RSS feeds
with open("rss.json", encoding="utf-8") as data_file:
    rss = json.load(data_file)

# Load general configuration
with open("config.json", encoding="utf-8") as config_file:
    config = json.load(config_file)
tz = pytz.timezone(config["timezone"])

# Create Discord client
client = discord.Client()
current_minute = datetime.datetime.now(tz).strftime("%H:%M")
server = None

# Main loop

async def main_loop():
    global current_minute
    global server
    await client.wait_until_ready()
    channel = None
    if config["debug_mode"]:
        channel = discord.Object(id=config["debug_channel_id"])
    else:
        channel = discord.Object(id=config["channel_id"])
    for s in client.servers:
        server = s
    while not client.is_closed:
        if current_minute != datetime.datetime.now(tz).strftime("%H:%M"):
            current_minute = datetime.datetime.now(tz).strftime("%H:%M")
            print(current_minute)
            await check_feeds(channel)
            await check_events(channel)
        await asyncio.sleep(config["refresh_interval"])

# Check for new events

async def check_events(channel):
    for event in reminders["events"]:
        if is_current(event["at"]):
            print("Event triggered: " + event["message"])
            await client.send_message(channel, event["message"]
                .replace("{notified_roles}"," ".join(str(role) for role in get_mentions(feed["notified_roles"]))))

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

# Check for new feeds

async def check_feeds(channel):
    global client
    global server
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
                message_queue.append(feed["message"]
                    .replace("{author}",item["author"])
                    .replace("{url}",item["link"])
                    .replace("{title}",item["title"])
                    .replace("{notified_roles}"," ".join(str(role) for role in get_mentions(feed["notified_roles"]))))
    for name in message_names:
        with open("rss-seen.txt","a+") as f:
            f.write(name + "\n")
    for message in message_queue:
        print("Feed notification: " + message)
        await client.send_message(channel, message)

# Respond to messages

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

# Utility functions

def get_mentions(roles):
    global server
    role_mentions = []
    if len(roles) > 0:
        for role in server.role_hierarchy:
            if role.name in roles:
                role_mentions.append(role.mention)
        if "everyone" in roles:
            role_mentions.append(server.default_role)
        if "here" in roles:
            role_mentions.append('@here')
    return role_mentions

# Run when ready

@client.event
async def on_ready():
    print("\nBIANCA DISCORD BOT")
    print("https://github.com/Nanofus/bianca")
    print("\nLogged in as")
    print(client.user.name)
    print(client.user.id)
    print("\n------\n")

# Start the program

while True:
    try:
        client.loop.create_task(main_loop())
        client.run(config["client_token"])
    except:
        pass
    else:
        break
