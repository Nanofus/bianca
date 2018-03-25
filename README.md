# Bianca
Bianca is a simple self-hosted [Discord](https://discordapp.com/) bot written in Python.

## Features
- Event reminders/"message of the days" with custom messages at specific times (once, every Friday, every year etc.)
- Notifications for any number of RSS/Atom feeds with custom messages
- Pinging specific roles, `@everyone` or `@here` whenever a reminder or RSS notification is posted

## Installation
1. `git clone https://github.com/Nanofus/bianca.git`
2. `pip install -r requirements.txt`
3. [Create a new bot](https://discordapp.com/developers/applications/me) and invite it to your server
4. Insert your text channel's ID and your bot's token into `config.json`
5. Run `run.bat` or `python bianca.py`

## Usage

- Add your RSS/Atom feeds into `rss.json`
- Add your event reminders and messages into `reminders.json`
  - Set the time for the message using prefixes as seen in the example file. The allowed prefixes are `WKD` (weekday), `DAY`, `MONTH`, `YEAR` and `TIME` (hours and minutes). When all of the defined values match the current time, the message is sent. Remember to always define `TIME`, otherwise the message is sent every minute.
- Change the timezone in `config.json`

Bianca has no commands inside Discord at the moment, but adding events and feeds through Discord is planned.
