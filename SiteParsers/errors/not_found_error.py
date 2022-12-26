from typing import Self

from SiteParsers.errors.base_parser_error import BaseParserError


class NotFoundError(BaseParserError):
    def __init__(self: Self, coin: str, ticker: str) -> Self:
        """Exception raised when an asset cannot be found.

        Args:
            coin: Full coin name(bitcoin, litecoin e.g.)
            ticker: Ticker of the coin(btc, ltc e.g.)
        """
        self.message = f"The asset({coin}, {ticker}) cannot be found"
        super().__init__(self.message)
