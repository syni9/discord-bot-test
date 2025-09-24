import os
import random
import discord
from discord import Embed
from discord.ext import commands
import nextcord
from nextcord.ext import commands
from osu import Client, GameModeStr
from google import genai
from dotenv import load_dotenv

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
discord_testing_guild_id = os.getenv("DISCORD_TESTING_GUILD_ID")
osu_client_secret = os.getenv("OSU_CLIENT_SECRET")
osu_client_id = os.getenv("OSU_CLIENT_ID")
gemini_api_key = os.getenv("GEMINI_API_KEY")

TESTING_GUILD_ID = discord_testing_guild_id
intents = nextcord.Intents.default()
intents.message_content = True

client_id = osu_client_id
client_secret = osu_client_secret
client_osu = Client.from_credentials(client_id, client_secret, None)

client = genai.Client(api_key=gemini_api_key)

bot = commands.Bot(command_prefix='!/', intents=intents)

def gamemode_translate_to_class(gamemode: str) -> GameModeStr:
    match gamemode:
        case "taiko":
            return GameModeStr.TAIKO
        case "standard":
            return GameModeStr.STANDARD
        case "catch":
            return GameModeStr.CATCH
        case "mania":
            return GameModeStr.MANIA
        case _:
            return "Invalid"
        
def gamemode_object_to_string(gamemode: GameModeStr) -> str:
    match gamemode:
        case GameModeStr.TAIKO:
            return "taiko" 
        case GameModeStr.STANDARD:
            return "standard"
        case GameModeStr.CATCH:
            return "catch"
        case GameModeStr.MANIA:
            return "mania"
        case _:
            return "Invalid"

def play_time_formatter(seconds: int) -> str:
    days = seconds / (3600 * 24)
    hours = (days % 1) * 24
    minutes = (hours % 1) * 60
    seconds = (minutes % 1) * 60
    return f'{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds'

def osu_profile(input: int | str, gamemode: str) -> discord.Embed:
    user = None
    user_global_rank = None
    user_country_rank = None
    if gamemode != None:
        user = client_osu.get_user(input, gamemode_translate_to_class(gamemode))
    else:
        user = client_osu.get_user(input)
        gamemode = gamemode_object_to_string(user.playmode)

    if (type(user.statistics.global_rank) != int) and (type(user.statistics.country_rank) != int):
        user_global_rank = "-"
        user_country_rank = "-"
    else:
        user_global_rank = format(user.statistics.global_rank, ",d")
        user_country_rank = format(user.statistics.country_rank, ",d")

    embed_user = discord.Embed(
        title=f'osu! {gamemode} Profile for {user.username}',
    )
    embed_user.set_thumbnail(url=user.avatar_url)
    embed_user.add_field(name="Username", value=user.username, inline=False)
    embed_user.add_field(name="Country", value=user.country.name, inline=False)
    embed_user.add_field(name="Performance Points", value=f'{user.statistics.pp:,.2f}', inline=False)
    embed_user.add_field(name="Global Rank", value=user_global_rank, inline=False)
    embed_user.add_field(name="Country Rank", value=user_country_rank, inline=False)
    embed_user.add_field(name="Total Play Time", value=play_time_formatter(user.statistics.play_time), inline=False)
    embed_user.add_field(name="Play Count", value=format(user.statistics.play_count, ",d"), inline=False)

    return embed_user

@bot.command()
async def getuserprofile(ctx: commands.context, arg: int | str, gm: str = None) -> Embed:
    await ctx.send(embed = osu_profile(arg, gm))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a * b)

def random_number_generator_matcherino(a, b):
        target = random.randint(a ,b)
        roll = random.randint(a, b)
        if target == roll:
            return f"You win, target: {target}, roll: {roll}"
        else:
            return f"You lost, target: {target}, roll: {roll}"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "gamble" in message.content.lower():
        await message.channel.send(random_number_generator_matcherino(0, 10))

    await bot.process_commands(message)

def gemini_answer_generator(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="in no more than 200 word" + prompt,
        )
    return response.text

@bot.command()
async def askgemini(ctx, arg):
    await ctx.send(gemini_answer_generator(arg))

bot.run(discord_token)
