from django.contrib import admin
from .models import Key, KeyDefinition, Enemy, Artifact, ArtifactDefinition
# Register your models here.

for m in (Key, KeyDefinition, Enemy, Artifact, ArtifactDefinition):
    admin.site.register(m)
