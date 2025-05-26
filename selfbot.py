print('MADE BY CHANDU')
from discord.ext import commands
import discord
import asyncio
import requests

token = "OTU1NDE5NjQwMTAyNzkzMjQ3.Gk78Mw.ZY2GGNZEzjq2LqzpfFuIN7t2adsE2U5iANFkuk"  # Apna token daal idhar

bot = commands.Bot(command_prefix=".", self_bot=True)

afk_status = {
    "enabled": False,
    "reason": "AFK"
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Ping command (real latency)
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{latency}ms`")
    await ctx.message.delete()

# Calculator command: !calc 5*10
@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Result: {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
    await ctx.message.delete()

# Spam command: !spam 5 Hello
@bot.command()
async def spam(ctx, times: int, *, msg):
    await ctx.message.delete()
    for _ in range(times):
        await ctx.send(msg)
        await asyncio.sleep(0.3)

# Purge command: !purge 10
@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    async for message in ctx.channel.history(limit=amount):
        try:
            await message.delete()
        except:
            pass

# AFK command: !afk reason
@bot.command()
async def afk(ctx, *, reason="AFK"):
    afk_status["enabled"] = True
    afk_status["reason"] = reason
    await ctx.send(f"**{ctx.author} is now AFK:** {reason}")
    await ctx.message.delete()

# LTC Price command
@bot.command()
async def ltc(ctx):
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd")
        price = res.json()["litecoin"]["usd"]
        await ctx.send(f"**Current Litecoin (LTC) Price:** ${price} USD")
    except Exception as e:
        await ctx.send(f"Error fetching LTC price: {e}")
    await ctx.message.delete()

# LTC Balance command
@bot.command()
async def bal(ctx):
    try:
        ltc_address = "LTb7gso7kvALydF3Rd755dr3CzUtAKc5if"

        # 1. LTC Wallet Info (Balance + Total Received)
        wallet_url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{ltc_address}"
        wallet_res = requests.get(wallet_url, timeout=10)

        # 2. LTC Price in USD
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
        price_res = requests.get(price_url, timeout=10)

        if wallet_res.status_code != 200 or price_res.status_code != 200:
            await ctx.send("Failed to fetch balance or price.")
            await ctx.message.delete()
            return

        wallet_data = wallet_res.json()
        price_data = price_res.json()

        balance_ltc = int(wallet_data["final_balance"]) / 1e8
        total_received_ltc = int(wallet_data["total_received"]) / 1e8
        ltc_usd = price_data["litecoin"]["usd"]

        balance_usd = round(balance_ltc * ltc_usd, 2)
        total_received_usd = round(total_received_ltc * ltc_usd, 2)

        msg = (
            f"**Litecoin Wallet Info**\n"
            f"> **Balance:** {balance_ltc} LTC (~${balance_usd} USD)\n"
            f"> **Total Received:** {total_received_ltc} LTC (~${total_received_usd} USD)"
        )

        await ctx.send(msg)

    except Exception as e:
        await ctx.send(f"Error: `{e}`")

    await ctx.message.delete()


# Back command: !back
@bot.command()
async def back(ctx):
    if afk_status["enabled"]:
        afk_status["enabled"] = False
        await ctx.send(f"**{ctx.author} is now back!**")
        await ctx.message.delete()

# Tag detection for AFK
@bot.event
async def on_message(message):
    if (
        afk_status["enabled"]
        and bot.user in message.mentions
        and message.author != bot.user
    ):
        await message.channel.send(f"{afk_status['reason']}")
    await bot.process_commands(message)

# Selfbot launch
bot.run(token)