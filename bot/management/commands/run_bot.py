from bot.bot import CustomClient, Bot
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Run bot'

    def handle(self, *args, **kwargs):
        bot = Bot(name="Gandalf")
        client = CustomClient(special_bot=bot)
        print("Initialized client...")
        client.run(settings.DISCORD_TOKEN)
        