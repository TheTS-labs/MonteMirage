from typing import Self


class BaseSiteParser(object):
    def __init__(self: Self, coin: str, ticker: str) -> Self:
        """Use given information (Coin and Ticker) to get the price of the asset.

        Args:
            coin: Full coin name(bitcoin, litecoin e.g.)
            ticker: Ticker of the coin(btc, ltc e.g.)
        """
        self.coin = coin
        self.ticker = ticker

    def get(self: Self) -> str:
        """Get the price and return a string with the price in dollars."""  # noqa: DAR401
        raise NotImplementedError()
