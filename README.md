# Bianca
Bianca is a simple [Discord](https://discordapp.com/) bot.

## Features
- Event reminders/"message of the days" with custom messages at specific times (once, every Friday, every year etc.)
- Notifications for any number of RSS feeds with custom messages

## Installation
1. `git clone https://github.com/Nanofus/bianca.git`
2. `pip install discord`
3. `pip install pytz`
4. `pip install feedparser`
5. [Create a new bot](https://discordapp.com/developers/applications/me) and invite it to your channel
6. Insert your text channel's ID and your bot's token into `config.json`
7. Run `run.bat`

## Usage

- Add your RSS feeds into `rss.json`
- Add your event reminders into `reminders.json`

Bianca has no commands inside Discord at the moment.
