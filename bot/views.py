from django.shortcuts import render
from .models import Key, KeyDefinition, Artifact, ArtifactDefinition
from asgiref.sync import sync_to_async


