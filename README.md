# MonteMirage

 Discord bot to check prices of crypto-assets

## 💿 Install and Run

1. Clone the repo with git:

```bash
  git clone https://github.com/TheTS-labs/MonteMirage.git
```

2. Rename .env.simple to .env and change the parameters if needed (more about the parameters in [Configuration](##-⚙️-configuration))

3. Run with `docker-compose`:

```bash
  docker-compose up
```

4. Done 🥳

## ⚙️ Configuration

You can customize the bot with a .env file:

- `POSTGRES_DATABASE` - Postgres database name(`docker-compose will use this variable`)
- `POSTGRES_USER` - Postgres username(`docker-compose will use this variable`)
- `POSTGRES_PASS` - Postgres user password(`docker-compose will use this variable`)
- `POSTGRES_HOST` - Postgres host, this variable is used by the app, if you want to use the database from `docker-copmose` leave it as `db`
- `POSTGRES_PORT` - Postgres port, this variable is used by the app and **does NOT affect the database from `docker-compose`**
- `POSTGRES_HOST_AUTH_METHOD` - [More on this in the Postgres README](https://github.com/docker-library/docs/blob/master/postgres/README.md#postgres_host_auth_method)
- `DISCORD_API_KEY` - API key from Discord
- `PARSE_ONCE_AT_SECS` - The watchlist assets are polled once in a certain time, and this variable defines this time(in seconds)
- `WATCHLIST` - The watchlist, Assets for which historical information is recorded once in `PARSE_ONCE_AT_SECS`, the format of string is `"coin#ticker coin#ticker"`, for example, `"bitcoin#btc litecoin#ltc dogecoin#doge"`, **space is a mandatory separator. If the asset in the watchlist is not found on one of the exchanges, the `NotFoundError` exception will be raised**

## Usage

Discord bot provides several commands:

- `!overview <coin:str> <ticker:str>` - Gets prices from all exchanges, if an asset is recorded in the `watchlist` and for it there is historical information will be recorded also `stdev` and `average` of prices between exchanges
- `!<exchange> <coin:str> <ticker:str>` - Gets the price from exact exchange
  - `!GateIO <coin:str> <ticker:str>` - Gets the price from GateIO
  - `!CoinMarketCap <coin:str> <ticker:str>` - Gets the price from CoinMarketCap
