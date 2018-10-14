# Pi - A Telegram bot

Pi that adds little more fun to group chats.

## Getting Started

Clone the repository

```
git clone https://github.com/harsh8398/Pi-telegram-bot.git
```

### Prerequisites

You can install all the prerequisites by following command in project directory.

```
pip install -r requirements
```

urbandictionary is needed to be installed from this [link](https://github.com/harsh8398/urbandictionary-py). Official version won't work as its tweaked for this bot.

### Setting up environment

To have bot running you need to set environment variable named 'TELEGRAM_TOKEN' (for master branch) or 'TELEGRAM_TOKEN_BETA' (for dev branch)

In linux you can set it by running following command

```
export TELEGRAM_TOKEN='tOkeN_ValUe_hERe'
```

Now you can make the bot live by running
```
python Pi.py
```

## APIs used

* [urbandictionary](https://www.urbandictionary.com/) - Used to fetch slangs
* [icndb](http://www.icndb.com/api/) - Used to fetch jokes

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details
