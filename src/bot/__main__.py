from bot.config import config
from bot.logging_config import setup_logging
from bot.bot import MyBot

def main() -> None:
    setup_logging(config.log_level)
    bot = MyBot(command_prefix=config.command_prefix)
    bot.run(config.discord_token)

if __name__ == "__main__":
    main()
