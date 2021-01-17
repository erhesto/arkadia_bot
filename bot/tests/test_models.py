import pytest
from bot.models import Key
from datetime import timedelta
from django.utils import timezone


@pytest.mark.django_db
def test_add_items_durability(key_factory):
    key = key_factory()
    key.durability = "bardzo dlugo"
    key.save()
    assert len(Key.objects.available()) == 1


@pytest.mark.django_db
def test_create_key_with_durability(key_definition_factory):
    definition = key_definition_factory()
    key = Key.objects.create_item_with_durability(definition=definition, durability="bardzo dlugo")
    assert len(Key.objects.available()) == 1


@pytest.mark.django_db
def test_key_might_be_expired(key_definition_factory):
    definition = key_definition_factory()
    key = Key.objects.create_item_with_durability(definition=definition, durability="bardzo krotko")
    assert len(Key.objects.might_be_expired()) == 1
    assert len(Key.objects.available()) == 1
    assert len(Key.objects.present()) == 0


@pytest.mark.django_db
def test_key_is_expired(key_factory):
    key = key_factory(durability_high=timezone.now()-timedelta(hours=10))
    assert len(Key.objects.expired()) == 1
