import discord
from .models import Key, Artifact, ArtifactDefinition, KeyDefinition
from .utils import Inventory, Parser, DURABILITIES


class CustomClient(discord.Client):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)
        self._bot = options.get('special_bot')
    
    async def on_message(self, message):
        await self._bot.dispatch_message(message, self.user)

    async def on_ready(self):
        for guild in self.guilds:
            print(f"Connected to: {guild.name}")


class Bot:
    """
    Interface:
        /pomoc
        /przejrzyj skrzynie
        /przejrzyj zapamietane
        /info ciezki stalowy klucz
        /dodaj [bron/bizuterie/zbroje/klucz] lekka krasnoludzka bajdana, bardzo dlugo [, utopce]
        /zapamietaj [zbroje/bron/bizuterie/klucz] lekka krasnoludzka bajdana, chroni przed obrazeniami fizycznymi
    """
    ARTIFACT_TYPES = {'zbroje', 'bron', 'bizuterie'}
    KEY_TYPES = {'klucz'}
    KNOWN_TYPES = ARTIFACT_TYPES.union(KEY_TYPES)
    COMMANDS = {'/przejrzyj', '/dodaj', '/zapamietaj', '/pomoc', '/info'}

    def __init__(self, name):
        self.name = name
        self.parser = Parser(self.COMMANDS)
    
    async def dispatch_message(self, message, user):
        if message.author == user or not message.content.startswith('/'):
            return
        try:
            parsed_command = self.parser.parse(message.content)
        except Exception as e:
            print(e)
            await message.channel.send("Blad parsowania komendy!")
        else:
            if parsed_command.command == '/przejrzyj' and parsed_command.item_type == 'skrzynie':
                await self.check_inventory(message)
            elif parsed_command.command == '/przejrzyj' and parsed_command.item_type == 'zapamietane':
                await self.check_known_items(message)
            elif parsed_command.command == '/dodaj':
                await self.add_item(message, parsed_command)
            elif parsed_command.command == '/zapamietaj':
                await self.add_definition(message, parsed_command)
            elif parsed_command.command == '/info':
                await self.get_info(message, parsed_command)
            elif parsed_command.command == '/pomoc':
                await self.help(message)
            else:
                await self.unknown_message(message)
    
    @property
    def inventory(self):
        return Inventory(key_model=Key, artifact_model=Artifact, key_definition=KeyDefinition, artifact_definition=ArtifactDefinition)

    async def unknown_message(self, message):
        await message.channel.send("Nie wiem o czym mowisz. Aby uzyskac pomoc wpisz: '/pomoc'.")
    
    async def check_inventory(self, message):
        await message.channel.send(await self.inventory.show())

    async def check_known_items(self, message):
        await message.channel.send(await self.inventory.show_known())

    async def add_item(self, message, parsed_command):
        if parsed_command.item_type not in self.KNOWN_TYPES:
            result = f"Nie znam takiego typu przedmiotu! Potrafie zapamietac: {','.join(self.KNOWN_TYPES)}."
        elif parsed_command.item_type in self.KNOWN_TYPES and parsed_command.additional_info is None:
            result = f"Brak informacji o przetrwalnosci sprzetu! Wpisz /pomoc by otrzymac poprawny sposob zapisu komendy."
        elif parsed_command.item_type in self.KNOWN_TYPES and parsed_command.additional_info[0] not in DURABILITIES:
            result = f"Niewlasciwa przetrwalnosc sprzetu. Wybierz sposrod: {', '.join(DURABILITIES.keys())}"
        elif parsed_command.item_type in self.ARTIFACT_TYPES:
            durability, *additional_info = parsed_command.additional_info
            additional_info = additional_info[0] if additional_info else ''
            result = await self.inventory.add_item(short=parsed_command.item_desc, durability=durability, additional_info=additional_info)
        else:
            durability, *additional_info = parsed_command.additional_info
            additional_info = additional_info[0] if additional_info else ''
            result = await self.inventory.add_key(short=parsed_command.item_desc, durability=durability, additional_info=additional_info)
        await message.channel.send(result)

    async def add_definition(self, message, parsed_command):
        if parsed_command.item_type not in self.KNOWN_TYPES:
            result = f"Nie znam takiego typu przedmiotu! Potrafie zapamietac: {', '.join(self.KNOWN_TYPES)}."
        elif parsed_command.item_type in self.ARTIFACT_TYPES and parsed_command.additional_info is None:
            result = "Dodaj informacje o magii zakletej w przedmiocie!"
        elif parsed_command.item_type in self.KEY_TYPES and parsed_command.additional_info is None:
            result = "Dodaj informacje o miejscu do ktorego prowadzi klucz!"
        elif parsed_command.item_type in self.ARTIFACT_TYPES:
            result = await self.inventory.add_known_artifact(short=parsed_command.item_desc, magic_power=parsed_command.additional_info[0])
        else:
            result = await self.inventory.add_known_key(short=parsed_command.item_desc, destination=parsed_command.additional_info[0]) 
        await message.channel.send(result)

    async def get_info(self, message, parsed_command):
        print(parsed_command.item_type)
        await message.channel.send(await self.inventory.get_info(short=parsed_command.item_desc))

    async def help(self, message):
        await message.channel.send(self.__doc__)
    