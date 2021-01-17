import uuid
from django.db import models
from django.utils.timezone import now, localtime
from .queryset import ItemManager, ItemQuerySet
from .utils import calculate_durability


class ItemDefinition(models.Model):
    short = models.CharField(max_length=120, db_index=True, unique=True, blank=False, null=False)
    description = models.TextField(default='', blank=True)

    class Meta:
        abstract = True

    def show(self):
        return self.short

class KeyDefinition(ItemDefinition):
    number_of_pieces = models.PositiveIntegerField(default=1)
    destination = models.CharField(max_length=256)

    def show(self):
        return f'{self.short} ({self.destination})'

class ArtifactDefinition(ItemDefinition):
    class ArtifactType(models.TextChoices):
        WEAPON = 'WEAPON', 'bron'
        ARMOR = 'ARMOR', 'zbroja'
        JEWELRY = 'JEWELRY', 'bizuteria'

    magic_power = models.CharField(max_length=256)
    artifact_type = models.CharField(max_length=96, choices=ArtifactType.choices, blank=True, default='')

    def show(self):
        return f'{self.short} ({self.magic_power})'

class Item(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    durability_low = models.DateTimeField(default=now)
    durability_high = models.DateTimeField(default=now)
    origin = models.CharField(max_length=256)

    objects = ItemManager.from_queryset(ItemQuerySet)()

    class Meta:
        abstract = True
        ordering = ['-durability_low']
    
    def __str__(self) -> str:
        return self.definition.short

    def show(self):
        return f'{self.definition.short} - {self.durability}'

    @property
    def durability(self) -> str:
        return f'({localtime(self.durability_low).strftime("%A %d.%m %H:%M")} - {localtime(self.durability_high).strftime("%A %d.%m %H:%M")}) (pozostalo {self.days_left} dni)'
    
    @durability.setter
    def durability(self, value):
        low, high = calculate_durability(value)
        self.durability_low = self.date_added + low
        self.durability_high = self.date_added + high

    @property
    def days_left(self):
        return (self.durability_low - now()).days + 1


class Key(Item):
    definition = models.ForeignKey(KeyDefinition, on_delete=models.CASCADE)


class Artifact(Item):
    definition = models.ForeignKey(ArtifactDefinition, on_delete=models.CASCADE)
