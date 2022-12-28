from datetime import datetime
from statistics import mean, stdev
import asyncio
from typing import List

from constants import DB, OVERVIEW_SRCS, PARSE_ONCE_AT_SECS, WATCHLIST
from models.historical_data import HistoricalOverview, HistoricalSrcPrice


def _get_price_from_all_srcs(coin: str, ticker: str) -> List:
    """Get prices for a specific coin by all sources.

    Args:
        coin: Full coin name(bitcoin, litecoin e.g.)
        ticker: Ticker of the coin(btc, ltc e.g.)

    Returns:
        Iterable HistoricalSrcPrice data dict
    """
    data_dicts = []

    for src in OVERVIEW_SRCS:
        price = float(src(coin, ticker).get().replace(",", ""))

        data_dicts.append({
            "price": price,
            "src": src.__name__,
            "coin": coin,
            "ticker": ticker,
            "timestamp": datetime.timestamp(datetime.now()),
        })

    return data_dicts


def _get_prices() -> List:
    """Get prices for a specific coin.

    Returns:
        List with two iterable data dicts
    """
    overview_data_dicts = []
    srcprices_data_dicts = []

    for coin, ticker in WATCHLIST:
        srcprices_data_dict = _get_price_from_all_srcs(coin, ticker)

        overview_data_dicts.append({
            "std_between_srcs": stdev([price["price"] for price in srcprices_data_dict]),
            "mean_between_srcs": mean([price["price"] for price in srcprices_data_dict]),
            "coin": coin,
            "ticker": ticker,
            "timestamp": datetime.timestamp(datetime.now()),
        })
        srcprices_data_dicts.extend(srcprices_data_dict)

    return [srcprices_data_dicts, overview_data_dicts]


async def update_prices() -> None:
    """Write updated prices into the DB."""
    while True:  # noqa: WPS457
        data_dicts = _get_prices()

        with DB.atomic():
            for price in data_dicts[0]:
                HistoricalSrcPrice.create(**price).save()
            for overview in data_dicts[1]:
                HistoricalOverview.create(**overview).save()

        await asyncio.sleep(PARSE_ONCE_AT_SECS)
