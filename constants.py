import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from peewee import PostgresqlDatabase

from SiteParsers.coinmarketcap import CoinMarketCap
from SiteParsers.gateio import GateIO

load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.message_content = True
BOT = commands.Bot(command_prefix="!", intents=INTENTS)
OVERVIEW_SRCS = (GateIO, CoinMarketCap)
DB = PostgresqlDatabase(
    os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASS"),
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT")),
)

# "bitcoin#btc litecoin#ltc" -> (["bitcoin", "btc"],
#                                ["litecoin", "ltc"])
WATCHLIST = [i.split("#") for i in os.getenv("WATCHLIST").split(" ")]  # noqa: WPS221, WPS111, WPS407
PARSE_ONCE_AT_SECS = float(os.getenv("PARSE_ONCE_AT_SECS"))
