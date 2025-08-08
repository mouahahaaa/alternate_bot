import os
from .bot import Bot
from dotenv import load_dotenv
from .cogs.base import BaseCog
from .cogs.nim import NimCog
from .cogs.chafer_crit import AraKritCog
from .log import logger_init, get_logger

if __name__ == "__main__":
    load_dotenv()
    logger_init()
    logger = get_logger()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("DISCORD_TOKEN variable is not set.")
        exit(1)
    cogs = [
        BaseCog(),
        NimCog(),
        AraKritCog(),
    ]
    bot = Bot(cogs, logger)
    bot.run(token)
