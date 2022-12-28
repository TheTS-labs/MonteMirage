from time import sleep
from datetime import datetime
from statistics import mean, stdev
from typing import List

from constants import DB, OVERVIEW_SRCS, PARSE_ONCE_AT_SECS, WATCHLIST
from models.historical_data import HistoricalOverview, HistoricalSrcPrice


def get_price_from_all_srcs(coin: str, ticker: str) -> List:
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


async def update_prices() -> None:
    while True:  # noqa: WPS457
        overview_data_dicts = []
        srcprices_data_dicts = []

        for coin, ticker in WATCHLIST:
            srcprices_data_dict = get_price_from_all_srcs(coin, ticker)

            overview_data_dicts.append({
                "std_between_srcs": stdev([price["price"] for price in srcprices_data_dict]),
                "mean_between_srcs": mean([price["price"] for price in srcprices_data_dict]),
                "coin": coin,
                "ticker": ticker,
                "timestamp": datetime.timestamp(datetime.now()),
            })
            srcprices_data_dicts.extend(srcprices_data_dict)

        with DB.atomic():
            for price in srcprices_data_dicts:
                HistoricalSrcPrice.create(**price).save()
            for overview in overview_data_dicts:
                HistoricalOverview.create(**overview).save()

        sleep(PARSE_ONCE_AT_SECS)
