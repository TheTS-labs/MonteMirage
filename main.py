import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from SiteParsers.coinmarketcap import CoinMarketCap
from SiteParsers.gateio import GateIO

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
overview_srcs = [GateIO, CoinMarketCap]


@bot.command(name="GateIO", help="Get the price of the asset in dollars, by GateIO")
async def gateio(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars, by GateIO.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    await ctx.reply("Current price of {coin}({ticker}) is: ${price}".format(
        coin=coin.capitalize(),
        ticker=ticker.upper(),
        price=GateIO(coin, ticker).get(),
    ))


@bot.command(name="CoinMarketCap", help="Get the price of the asset in dollars, by CoinMarketCap")
async def coinmarketcap(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    await ctx.reply("Current price of {coin}({ticker}) is: ${price}".format(
        coin=coin.capitalize(),
        ticker=ticker.upper(),
        price=CoinMarketCap(coin, ticker).get(),
    ))


@bot.command(name="overview", help="Get the price of the asset in dollars, by all src`s")
async def overview(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars, by all src`s.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    reply = [f"Overview of {coin}({ticker}):"]

    for overview_src in overview_srcs:
        reply.append("\n- By {name}, price is: ${price}".format(
            name=overview_src.__name__,
            price=overview_src(coin, ticker).get(),
        ))

    await ctx.reply("".join(reply))

bot.run(os.getenv("DISCORD_API_KEY"))
