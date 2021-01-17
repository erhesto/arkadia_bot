from datetime import timedelta
from asgiref.sync import sync_to_async
from itertools import chain
from dataclasses import dataclass


DURABILITIES = {
        "naprawde dlugo": (timedelta(days=8), timedelta(days=8)),
        "bardzo dlugo": (timedelta(days=5), timedelta(days=8)),
        "dlugo": (timedelta(days=3), timedelta(days=5)),
        "raczej dlugo": (timedelta(days=2), timedelta(days=3)),
        "troche": (timedelta(days=1), timedelta(days=2)),
        "raczej krotko": (timedelta(hours=6), timedelta(days=1)),
        "krotko": (timedelta(hours=1), timedelta(hours=6)),
        "bardzo krotko": (timedelta(hours=0), timedelta(hours=1)),
}


@dataclass
class ParsedCommand:
    command: str
    item_type: str = ''
    item_desc: str = ''
    additional_info: list = None


class Parser:
    def __init__(self, known_commands):
        self._known_commands = known_commands
    
    def parse(self, line: str):
        if not line.startswith('/'):
            raise ValueError("It's not a command!")
        
        command, *rest = line.split(' ', maxsplit=1)

        if command not in self._known_commands:
            raise ValueError("Unknown command!")

        if not rest:
            return ParsedCommand(command=command)
        
        if command == '/info':
            return ParsedCommand(command=command, item_desc=rest[0])
        
        item_type, *rest = rest[0].split(' ', maxsplit=1)

        if not rest:
            return ParsedCommand(command=command, item_type=item_type)
        
        item_desc, *rest = [x.strip() for x in rest[0].split(',')]

        if not rest:
            return ParsedCommand(command=command, item_type=item_type, item_desc=item_desc)
        else:
            return ParsedCommand(command=command, item_type=item_type, item_desc=item_desc, additional_info=rest)


def calculate_durability(durability):
    return DURABILITIES.get(durability, DURABILITIES['bardzo krotko'])


class InventorySection:
    def __init__(self, heading, objects):
        self.heading = heading
        self.objects = objects

    def __str__(self):
        obj_descs = '\n'.join(f'\t\t- {obj.show()}' for obj in self.objects) or '\t\tTa sekcja jest w tym momencie pusta.'
        return f'\t{self.heading}:\n{obj_descs}\n'



class Inventory:
    def __init__(self, **kwargs):
        self.key = kwargs['key_model']
        self.artifact = kwargs['artifact_model']
        self.key_definition = kwargs['key_definition']
        self.artifact_definition = kwargs['artifact_definition']

        self.heading = kwargs.get('heading', "W tym momencie w skrzyni znajduja sie:")
        self.known_heading = kwargs.get('known', "Zapamietane klucze i artefakty:")
        self.keys = InventorySection('Klucze', self.key.objects.present())
        self.artifacts = InventorySection('Artefakty', self.artifact.objects.present())
        self.soon_expire = InventorySection(
            'Mogly zniknac', 
            chain(self.artifact.objects.might_be_expired(), self.key.objects.might_be_expired())
        )
        self.known_keys = InventorySection('Klucze', self.key_definition.objects.all())
        self.known_artifacts = InventorySection('Artefakty', self.artifact_definition.objects.all())

    @sync_to_async
    def show(self):
        return '\n'.join(
            str(section)
            for section in [self.heading, self.keys, self.artifacts, self.soon_expire]
        )

    @sync_to_async
    def show_known(self):
        return '\n'.join(
            str(section)
            for section in [self.known_heading, self.known_keys, self.known_artifacts]
        )
    
    @sync_to_async
    def add_known_artifact(self, short, magic_power):

        obj, created = self.artifact_definition.objects.get_or_create(
            short=short, 
        )
        obj.magic_power = magic_power
        obj.save()
        if created:
            return f'Zapamietalem informacje o {short}.'
        else:
            return f'Zaktualizowalem informacje o {short}!'

    @sync_to_async
    def add_known_key(self, short, destination):

        obj, created = self.key_definition.objects.get_or_create(
            short=short,  
        )
        obj.destination = destination
        obj.save()
        if created:
            return f'Zapamietalem informacje o {short}.'
        else:
            return f'Zaktualizowalem informacje o {short}!'

    @sync_to_async
    def add_item(self, short, durability, additional_info):
        try:
            definition = self.artifact_definition.objects.get(short=short)
        except self.artifact_definition.DoesNotExist:
            return f'Nie znam zadnego artefaktu zgodnego z opisem: {short}'
        else:
            obj = self.artifact.objects.create_item_with_durability(durability=durability, origin=additional_info, definition=definition)
            return f'Dodano {obj.definition.short} o id: {obj.uuid} ktory przetrwa do {obj.durability}'
    
    @sync_to_async
    def add_key(self, short, durability, additional_info):
        try:
            definition = self.key_definition.objects.get(short=short)
        except self.key_definition.DoesNotExist:
            return f'Nie znam zadnego klucza zgodnego z opisem: {short}'
        else:
            obj = self.key.objects.create_item_with_durability(durability=durability, origin=additional_info, definition=definition)
            return f'Dodano {obj.definition.short} o id: {obj.uuid} ktory przetrwa do {obj.durability}'
    
    @sync_to_async
    def get_info(self, short):
        if (artifact := self.artifact_definition.objects.filter(short=short).first()) is not None:
            return f'Przedmiot: {artifact.short}\nOpis: {artifact.description or "Brak opisu"}\nSpecjalne wlasciwosci: {artifact.magic_power}'
        elif (key := self.key_definition.objects.filter(short=short).first()) is not None:
            return f'Przedmiot: {key.short}\nOpis: {key.description or "Brak opisu"}\nProwadzi do: {key.destination}\nLiczba czesci: {key.number_of_pieces}'
        else:
            return 'Nie znam takiego przedmiotu!'
    