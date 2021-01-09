from .models import Key, KeyDefinition, Enemy, Artifact, ArtifactDefinition
from django.utils import timezone


class Bot:
    def __init__(self, name) -> None:
        self.name = name
    
    def get_available_items(self, model):
        model.objects.available()
    
    def get_near_expirations(self, model):
        model.objects.might_be_expired()

    