import asyncio
import logging
import os

import discord
from discord.ext import commands

from constants import BOT, DB, OVERVIEW_SRCS
from models.historical_data import HistoricalOverview, HistoricalSrcPrice
from SiteParsers.coinmarketcap import CoinMarketCap
from SiteParsers.errors.not_found_error import NotFoundError
from SiteParsers.gateio import GateIO
from update_prices import update_prices


def get_change(current: float | int, previous: float | int) -> float:
    """Calculate percent change between two numbers.

    Args:
        current: Current number
        previous: Previous number

    Returns:
        Float number with two numbers after comma
    """
    if current == previous:
        return 100.0
    try:
        return round((abs(current - previous) / previous) * 100.0, 2)
    except ZeroDivisionError:
        return 0


@BOT.command(name="GateIO", help="Get the price of the asset in dollars, by GateIO")
async def gateio(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars, by GateIO.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    previous_price = HistoricalSrcPrice.select().where(
        HistoricalSrcPrice.src == "GateIO",
        HistoricalSrcPrice.coin == coin,
        HistoricalSrcPrice.ticker == ticker,
    ).first()

    try:
        current_price = float(GateIO(coin, ticker).get().replace(",", ""))
    except NotFoundError as err:
        await ctx.reply(err.message)
        return

    if previous_price:
        change = get_change(current_price, previous_price.price)

        await ctx.reply("Current price of {coin}({ticker}) is: ${price}({change_symbol}{change}%)".format(
            coin=coin.capitalize(),
            ticker=ticker.upper(),
            price=current_price,
            change_symbol="+" if current_price >= previous_price.price else "-",
            change=change,
        ))
    else:
        await ctx.reply("Current price of {coin}({ticker}) is: ${price}".format(
            coin=coin.capitalize(),
            ticker=ticker.upper(),
            price=current_price,
        ))


@BOT.command(name="CoinMarketCap", help="Get the price of the asset in dollars, by CoinMarketCap")
async def coinmarketcap(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars, by CoinMarketCap.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    previous_price = HistoricalSrcPrice.select().where(
        HistoricalSrcPrice.src == "CoinMarketCap",
        HistoricalSrcPrice.coin == coin,
        HistoricalSrcPrice.ticker == ticker,
    ).first()

    try:
        current_price = float(CoinMarketCap(coin, ticker).get().replace(",", ""))
    except NotFoundError as err:
        await ctx.reply(err.message)
        return

    if previous_price:
        change = get_change(current_price, previous_price.price)

        await ctx.reply("Current price of {coin}({ticker}) is: ${price}({change_symbol}{change}%)".format(
            coin=coin.capitalize(),
            ticker=ticker.upper(),
            price=current_price,
            change_symbol="+" if current_price >= previous_price.price else "-",
            change=change,
        ))
    else:
        await ctx.reply("Current price of {coin}({ticker}) is: ${price}".format(
            coin=coin.capitalize(),
            ticker=ticker.upper(),
            price=current_price,
        ))


@BOT.command(name="overview", help="Get the price of the asset in dollars, by all src`s")
async def overview(ctx: commands.context.Context, coin: str, ticker: str) -> None:
    """Get the price of the asset in dollars, by all src`s.

    Args:
        ctx: Context object
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)
    """
    reply = [f"Overview of {coin.capitalize()}({ticker.upper()}):"]  # noqa: WPS221

    previous_record = HistoricalOverview.select().where(
        HistoricalOverview.coin == coin,
        HistoricalOverview.ticker == ticker,
    ).order_by(-HistoricalOverview.timestamp).first()

    if previous_record:
        reply.extend([
            "\n*Standard deviation(std) of price between exchanges: ${std}*".format(
                std=round(previous_record.std_between_srcs, 2),
            ),
            "\n*Average price between exchanges: ${mean}*\n".format(
                mean=round(previous_record.mean_between_srcs, 2),
            ),
        ])

    for overview_src in OVERVIEW_SRCS:
        try:
            reply.append("\n- By {name}, price is: ${price}".format(
                name=overview_src.__name__,
                price=overview_src(coin, ticker).get(),
            ))
        except NotFoundError as err:
            await ctx.reply(err.message)
            return

    await ctx.reply("".join(reply))


async def main() -> None:  # noqa: D103
    DB.connect()
    DB.create_tables([HistoricalSrcPrice, HistoricalOverview])
    discord.utils.setup_logging(level=logging.INFO, root=False)

    await asyncio.gather(
        BOT.start(os.getenv("DISCORD_API_KEY")),
        update_prices(),
    )
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Quiting...")  # noqa: WPS421
    finally:
        DB.close()
