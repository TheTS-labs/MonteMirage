import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from peewee import SqliteDatabase

from SiteParsers.coinmarketcap import CoinMarketCap
from SiteParsers.gateio import GateIO

load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.message_content = True
BOT = commands.Bot(command_prefix="!", intents=INTENTS)
OVERVIEW_SRCS = (GateIO, CoinMarketCap)
DB = SqliteDatabase("./app.sqlite", pragmas={"journal_mode": "wal", "cache_size": -1024 * 64})

# "bitcoin#btc litecoin#ltc" -> (["bitcoin", "btc"],
#                                ["litecoin", "ltc"])
WATCHLIST = [i.split("#") for i in os.getenv("WATCHLIST").split(" ")]  # noqa: WPS221, WPS111, WPS407
PARSE_ONCE_AT_SECS = float(os.getenv("PARSE_ONCE_AT_SECS"))
