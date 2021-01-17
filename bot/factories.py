import factory
import factory.fuzzy


class KeyDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'bot.KeyDefinition'
    
    short = factory.Faker('name')


class KeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'bot.Key'
    
    definition = factory.SubFactory(KeyDefinitionFactory)


