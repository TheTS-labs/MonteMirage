from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Parser(object):
    """Use given information (Coin, Ticker, Relation, Source, Config and Driver) to get the price of the asset."""

    def __init__(self, template_args, src, config, driver):
        """Raise a zero division error or type error.

        Args:
            template_args: Dict with Coin, Ticker, Relation parameters
            src: Source of data
            config: List of configurations
            driver: Selenium WebDriver

        Raises:
            Exception: If the src configuration is outdated
        """
        self.templateArgs = template_args
        self.config = config[src]
        self.driver = driver

        if self.config["Version"] != 3:
            raise Exception("VersionError")  # noqa: WPS454

    def get(self):
        """Get the page and searche for data.

        Returns:
            List of Price and Relation
        """
        try:  # noqa: WPS229 Because the code expects ANY exceptions
            self.driver.get(
                self.config["URLTemplate"][0].format(**self._delete_unused_template_args()),
            )

            self._check_not_found()

            return [
                self._get_element_text(WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((
                        By.XPATH, self.config["PriceXPath"],
                    )),
                )),
                self._get_element_text(WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((
                        By.XPATH, self.config["RelationSymbolXPath"],
                    )),
                )),
            ]
        except Exception as exc:
            self._on_error(exc)

    def warnings(self):
        """Return a list of all warnings defined by the configuration.

        # noqa: DAR201
        """
        return self.config["Warnings"]

    def _delete_unused_template_args(self):
        return {key: self.templateArgs[key] for key in self.config["URLTemplate"][1]}

    def _check_not_found(self):
        if self.config["Capabilities"]["CausesNotFound"]:
            if self.driver.status_code() == 404:  # noqa: WPS432 Because it's Not Found HTTP code
                raise Exception("CoinNotFound")  # noqa: WPS454
        elif self.config["NotFoundText"] in self.driver.page_source:
            self._on_error(Exception("Coin not found or address no longer exists"))

    def _on_error(self, exc):
        raise exc

    def _get_element_text(self, web_element):
        element_text = web_element.text  # sometime NOT work

        if not element_text:
            element_text = web_element.get_attribute("innerText")

        if not element_text:
            element_text = web_element.get_attribute("textContent")

        return element_text
