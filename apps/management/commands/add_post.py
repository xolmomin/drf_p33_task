import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import Post, Category


class Command(BaseCommand):
    help = "Bu komanda post qoshish uchun "

    def add_arguments(self, parser):
        parser.add_argument("n", type=int)

    def handle(self, *args, **kwargs):
        count = kwargs['n']
        faker = Faker()

        category_list = []
        for _ in range(10):
            new_category = Category.objects.create(
                name=faker.text(max_nb_chars=25)
            )
            category_list.append(new_category)

        for _ in range(count):
            Post.objects.create(
                userId=random.randint(5, 100),
                title=faker.paragraph(nb_sentences=2),
                category=random.choice(category_list),
                type=random.choice(Post.Type.choices)[0],
                body=faker.paragraph(nb_sentences=10)
            )
        self.stdout.write(self.style.SUCCESS(f"{count} ta Post Qo'shildi"))
