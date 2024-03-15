## Telegram messaging bot for ProPresenter
A small example on how you can create a bot for sending messages to ProPresenter using Telegram. I also added a shell file which can be used to run the script on startup. The `auth_token` is the value that should be passed when starting the bot, this is so that only people who should have access do actually have access for sending the messages.

### Requirements
- Python 3
- ProPresenter 7
- Python packages `python-telegram-bot`, `requests`
- Telegram bot using @botfather
- Setup config values in `messagesbot.py`

> [!CAUTION]
> This is just a rudimental example of how this can be achieved. There is a lot of things that can be improved on, I am aware of that!