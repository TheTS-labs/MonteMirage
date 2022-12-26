from typing import Self

import requests
from lxml import html  # noqa: S410

from SiteParsers.base_parser import BaseSiteParser
from SiteParsers.errors.not_found_error import NotFoundError


class GateIO(BaseSiteParser):
    def get(self: Self) -> str:
        """Get the price and return a string with the price in dollars.

        Returns:
            String with the price in dollars

        Raises:
            NotFoundError: If the asset cannot be found
        """
        page = requests.get(f"https://www.gate.io/price/{self.coin}-{self.ticker}/usd")  # noqa: WPS221
        soup = html.fromstring(page.content)

        if b"The page you are looking for is not found!" in page.content:
            raise NotFoundError(self.coin, self.ticker)

        return soup.xpath('//*[@id="quote-details"]/div[1]/div[2]/div[2]/span/span[2]')[0].text
