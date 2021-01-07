import uuid
from django.db import models
from datetime import timedelta
from django.utils.timezone import now


def calculate_durability(self, durability):
    durabilities = {
        "naprawde dlugo": (timedelta(days=8), timedelta(days=8)),
        "bardzo dlugo": (timedelta(days=5), timedelta(days=8)),
        "dlugo": (timedelta(days=3), timedelta(days=5)),
        "raczej dlugo": (timedelta(days=2), timedelta(days=3)),
        "troche": (timedelta(days=1), timedelta(days=2)),
        "raczej krotko": (timedelta(hours=6), timedelta(days=1)),
        "krotko": (timedelta(hours=1), timedelta(hours=6)),
        "bardzo krotko": (timedelta(hours=0), timedelta(hours=1)),
    }
    return durabilities.get(durability, durability['bardzo krotko'])


class Enemy(models.Model):
    class Toughness(models.TextChoices):
        EASY = 'EASY', 'Latwy'
        MEDIUM = 'MEDIUM', 'Sredni'
        HARD = 'HARD', 'Trudny'
        ULTRA_HARD = 'ULTRA_HARD', 'Bardzo trudny'
        EXTREME = 'EXTREME', 'Ekstremalnie ciezki'


    class Land(models.TextChoices):
        TILEA = 'TILEA', 'Tilea'
        EMPIRE = 'EMPIRE', 'Imperium'
        WE_MOUNTAINS = 'WE_MOUNTAINS', 'Gory Kranca Swiata'
        GREY_MOUNTAINS = 'GREY_MOUNTAINS', 'Gory Szare'
        BRETONIA = 'BRETONIA', 'Bretonia'

    name = models.CharField(max_length=256, unique=True)
    number_of_people = models.PositiveIntegerField(null=True)
    toughness = models.CharField(max_length=32, choices=Toughness.choices)
    land = models.CharField(max_length=32, choices=Land.choices, null=True)

    def __str__(self) -> str:
        return self.name

class ItemDefinition(models.Model):
    short = models.CharField(max_length=64, db_index=True, unique=True)
    description = models.TextField(null=True)

    class Meta:
        abstract = True

class KeyDefinition(ItemDefinition):
    number_of_pieces = models.PositiveIntegerField(default=1)
    destination = models.ForeignKey(Enemy, on_delete=models.CASCADE)


class ArtifactDefinition(ItemDefinition):
    class MagicPower(models.TextChoices):
        FIRE_DAMAGE = 'FIRE', 'Obrazenia od ognia'
        MAGIC_DAMAGE = 'MAGIC', 'Obrazenia od magii'

    class ArtifactType(models.TextChoices):
        WEAPON = 'WEAPON', 'bron'
        ARMOR = 'ARMOR', 'zbroja'
        JEWELRY = 'JEWELRY', 'bizuteria'

    magic_power = models.CharField(max_length=96, choices=MagicPower.choices)
    artifact_type = models.CharField(max_length=96, choices=ArtifactType.choices)
    description = models.TextField()


class ItemManager(models.Manager):
    def create_item_with_durability(self, *args, durability=None, **kwargs):
        if durability is not None:
            time_now = now()
            low, high = self.calculate_durability(durability)
            kwargs.update({'durability_low': time_now + low, 'durability_high': time_now + high})
        self.create(*args, **kwargs)


class Item(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    durability_low = models.DateTimeField(auto_now_add=True)
    durability_high = models.DateTimeField(auto_now_add=True)
    dropped_from = models.ForeignKey(Enemy, on_delete=models.SET_NULL, null=True)
    exchanged = models.BooleanField(default=False)
    exchanged_with = models.CharField(max_length=256, null=True, blank=True)

    objects = ItemManager

    class Meta:
        abstract = True

    @property
    def durability(self):
        return self.durability_high
    
    @durability.setter
    def durability(self, value):
        low, high = calculate_durability(value)
        self.durability_low = self.date_added + low
        self.durability_high = self.date_added + high

class Key(Item):
    definition = models.ForeignKey(KeyDefinition, on_delete=models.CASCADE)
    

class Artifact(Item):
    definition = models.ForeignKey(ArtifactDefinition, on_delete=models.CASCADE)
