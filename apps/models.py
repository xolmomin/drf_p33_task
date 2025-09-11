from django.db.models import Model, IntegerField, CharField, TextField, ForeignKey, CASCADE, TextChoices


class Category(Model):
    name = CharField(max_length=120)


class Post(Model):
    class Type(TextChoices):
        PREMIUM = 'premium', 'PREMIUM'
        STANDARD = 'standard', 'STANDARD'

    userId = IntegerField()
    category = ForeignKey('apps.Category', CASCADE)
    type = CharField(max_length=15, choices=Type.choices, default=Type.STANDARD)
    title = CharField(max_length=255)
    body = TextField()
