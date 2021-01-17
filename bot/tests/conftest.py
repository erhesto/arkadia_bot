from pytest_factoryboy import register
from bot.factories import KeyFactory, KeyDefinitionFactory

register(KeyFactory)
register(KeyDefinitionFactory)