# Title 

## About this project
This project is just a discord bot for me to mess around with and learn.

## Python packages used in this project
- **[nextcord](https://docs.nextcord.dev/en/stable/)**
- **[osu.py](https://osupy.readthedocs.io/en/v4.0.2/)**
- **[discord.py](https://discordpy.readthedocs.io/en/stable/)**
- **[Gemini API](https://ai.google.dev/gemini-api/docs/quickstart)**
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**
  
## How to run this I think
- Install the packages using pip install
- Create .env file in the directory and follow the variables below
```
GEMINI_API_KEY=gemini-api-key
DISCORD_TOKEN=discord-token
OSU_CLIENT_SECRET=osu-client-secret
OSU_CLIENT_ID=osu-client-id
DISCORD_TESTING-GUILD_ID=discord-testing-guild-id
```
- Replace the value with its appropriate API and the like
- **Gemini API key** found [here](https://aistudio.google.com/app/apikey)
- **Discord Token** found [here](https://discord.com/developers/applications)
  - this is also where you set up the bot, I think just follow nextcord documentation for this
- **osu! Client Secret and Client ID** found [here](https://osu.ppy.sh/home/account/edit)
  - browse to the OAuth section and create New OAuth Application
- **Discord Testing Guild ID** is just a discord server ID
  - may need to turn on Developer Mode found in Settings/App Settings/Advanced in discord
