from django.contrib import admin
from .models import Key, KeyDefinition, Artifact, ArtifactDefinition
# Register your models here.

for m in (Key, KeyDefinition, Artifact, ArtifactDefinition):
    admin.site.register(m)
