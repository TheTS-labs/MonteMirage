import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from site_parser import Parser

with open("./sites.yaml", "r") as stream:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    sp = Parser(
        {"Coin": "litecoin", "Ticker": "ltc", "Relation": "uah"},
        "GateIO",
        yaml.safe_load(stream),
        driver,
    )

    for warn in sp.warnings():
        print(f"- {warn}")  # noqa: WPS421

    print(sp.get())  # noqa: WPS421
