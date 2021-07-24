
BINANCE EMA TRADE BOT README

Hello, you want to trade crypto currencies in Binance without needing to
check the price changes all the time. This bot is for you.

To use the bot, you need to install python. If you are Linux or Mac user
you should be able to run python scripts from terminal without guidance.

Requirements: python 3, python-binance

--------------------------------------------------------------------------------------------------

WINDOWS INSTALLATION

But for you Windows users. Go to https://www.python.org/downloads/windows/
and download Python Windows Installer (64-bit) and install it after it
has downloaded.

Then open Powershell and use the command 'pip install python-binance' to
install Binance python API requirements for this script.

Then change lines 9 and 10 to include your Binance keys, which you can get
from Binance website by creating API keys.

Then in Powershell 'cd' to the location where you downloaded this bot scripts
and execute it with command 'python .\main.py --pair YOURPAIR'. Plus your
additional parameters.

To change settings of the bot you need to ctr+c end it and run the script
with different parameters.

The software currently supports only coins with 3 letters, so 6 letter pairs.


--------------------------------------------------------------------------------------------------

COMMAND PARAMETERS

--pair -c              The coin pair you trade on Binance "Required"
--candlestick -i       Length of the candlestick you want to use for MA calculations.
                       Values for candlestick: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h,
                       1d, 3d, 1w, 1mo, Default 1m.
--emaa -a              Smaller MA line value, such as default 7.
--emab -b              Bigger MA line value, such as default 25.
--length -l            How many candlesticks to use for calculating EMA. Default 30.
--max_amount -m        Max amount of first coin, to trade. Example 0.1 or 1.5
--open -o              Do you want to use open or closed price values. Default closed.
--allow_negative -n    Allow doing negative trades, which do not make profit. No parameters.
--allow_panic -p       Allow panic sell for the time of ticks you specify. No parameters.
--panic_ticks -t       How many candlesticks you check for panic sell. Default 1.
--get_pairs -g         Lists pairs used in Binance. No parameters. Does not start the bot.
--pair_search -s       Search a pair with 3 letter string. For example BTC.
--rounding -x          Round the trade amount to decimal places. Some pairs require maximum 2 decimals.
                       Default 3.
--help -h              Show this help. No parameters. Does not start the bot.


--------------------------------------------------------------------------------------------------

SOME EXTRA EXPLANATION

The minimum profit is 0.01% for the bot. Since that is what Binance takes from you
from trading. So if profit is more than 0.01% you make profit with your trades.

You can search pairs with --pair_search and supplying variable BTC or ETH for example
with the paramater. Otherwise just use --get_pairs to list all working pairs.

The allow_negative parameter allows the bot to make negative trades, but allow panic
allows the bot to make negative trades only inside certain amount of time. Which is
useful to handle small dips and raises of price when EMA changes fast from sell to
trade or otherwise. Without allow_panic the bot can get stuck for example, if it
sells before the price starts to really drop. So be advised when using allow_panic,
it allows negative trades. The allow_negative is useful if your bot gets stuck and
you want to restart trading with the bot.


--------------------------------------------------------------------------------------------------

CHANGELOG

1.1.0
  - Add --pair_search parameter to search supported coin pairs with the bot.
  - Add --max_amount parameter to limit trade amount of coin.
  - Add more profit calculations, all time, possible next trade, runtime
  - Pretty print the data

1.1.1
  - Fix starting trading without existing trade on coin pair


--------------------------------------------------------------------------------------------------

LICENSE

You use this software at your own risk, change at your own risk. I do not refund your
losses. I do not need your profits. It is a game of risk and up to your settings and
changes. So piss of ranting. I do not take any responsibility of you using this
piece of Binance EMA trading bot i have created for you to possibly profit.

Author: Toni Lukkaroinen

Tough you can send me extra coin, email me at toni.lukkaroinen@gmail.com
if you want to do that.
