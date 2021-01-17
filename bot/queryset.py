from django.db import models
from django.utils.timezone import now
from .utils import calculate_durability


class ItemManager(models.Manager):
    def create_item_with_durability(self, *args, durability=None, **kwargs):
        if durability is not None:
            time_now = now()
            low, high = calculate_durability(durability)
            kwargs.update({'durability_low': time_now + low, 'durability_high': time_now + high})
            print(kwargs)
        return self.create(*args, **kwargs)


class ItemQuerySet(models.QuerySet):
    def present(self):
        return self.filter(durability_low__gt=now())

    def available(self):
        return self.filter(durability_high__gt=now())

    def might_be_expired(self):
        return self.available().filter(durability_low__lt=now())
    
    def expired(self):
        return self.filter(durability_high__lt=now())
