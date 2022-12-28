from typing import Self

import requests
from lxml import html  # noqa: S410

from SiteParsers.base_parser import BaseSiteParser
from SiteParsers.errors.not_found_error import NotFoundError


class CoinMarketCap(BaseSiteParser):
    def get(self: Self) -> str:
        """Get the price and return a string with the price in dollars.

        Returns:
            String with the price in dollars

        Raises:
            NotFoundError: If the asset cannot be found
        """
        page = requests.get(f"https://coinmarketcap.com/currencies/{self.coin}/")  # noqa: WPS221
        soup = html.fromstring(page.content)

        if b"Sorry, we couldn't find your page" in page.content:
            raise NotFoundError(self.coin, self.ticker)

        try:
            return soup.xpath(
                '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span',
            )[0].text.replace("$", "")
        except IndexError:
            raise NotFoundError(self.coin, self.ticker)
