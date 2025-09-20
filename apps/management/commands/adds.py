import random

from django.core.management.base import BaseCommand
from faker.proxy import Faker

from apps.models import Order, OrderItem, User, Product, Category


class Command(BaseCommand):
    help = "Bu komanda malumot qoshish uchun"
    model_list = {'orders', 'orderitems', 'carts', 'cartitems', 'users', 'products', 'categories'}

    def add_arguments(self, parser):
        parser.add_argument('--orders', type=int)
        parser.add_argument('--orderitems', type=int)
        parser.add_argument('--carts', type=int)
        parser.add_argument('--cartitems', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--products', type=int)
        parser.add_argument('--categories', type=int)

    def _generate_orders(self, number: int):
        for _ in range(number):
            random_user_id = User.objects.values_list('id', flat=True).order_by('?').first()
            if random_user_id is None:
                self.stdout.write(self.style.ERROR("No user"))
                return
            Order.objects.create(user_id=random_user_id, total_amount=0)
        self.stdout.write(self.style.SUCCESS(f"Order generated - {number}"))

    def _generate_orderitems(self, number: int):
        for _ in range(number):
            random_order = Order.objects.order_by('?').first()
            random_product = Product.objects.order_by('?').first()
            _price = random.randint(10, 100) * 1000
            _quantity = random.randint(1, 10)
            OrderItem.objects.create(
                order=random_order,
                product=random_product,
                quantity=_quantity,
                price=_price
            )
            random_order.total_amount += _price * _quantity
            random_order.save()

        self.stdout.write(self.style.SUCCESS(f"Order Items generated - {number}"))

    def _generate_carts(self, number: int):
        pass

    def _generate_cartitems(self, number: int):
        pass

    def _generate_categories(self, number: int):
        for _ in range(number):
            Category.objects.create(name=self.faker.text(max_nb_chars=25))
        self.stdout.write(self.style.SUCCESS(f"Categories generated - {number}"))

    def _generate_users(self, number: int):
        for _ in range(number):
            User.objects.create(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                phone=self.faker.phone_number(),
            )
        self.stdout.write(self.style.SUCCESS(f"Users generated - {number}"))

    def _generate_products(self, number: int):
        for _ in range(number):
            random_category_id = Category.objects.values_list('id', flat=True).order_by('?').first()
            if random_category_id is None:
                self.stdout.write(self.style.ERROR('No category'))
                return
            Product.objects.create(
                name=self.faker.text(max_nb_chars=15),
                description=self.faker.text(max_nb_chars=25),
                image=self.faker.image_url(),
                price=random.randint(10, 500) * 1000,
                category_id=random_category_id,
            )
        self.stdout.write(self.style.SUCCESS(f"Products generated - {number}"))

    def handle(self, *args, **kwargs):
        self.faker = Faker('uz_Uz')
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        generated_item_names = set(kwargs).intersection(self.model_list)

        for _name in generated_item_names:
            getattr(self, f"_generate_{_name}")(kwargs[_name])
