import random

from django.core.management.base import BaseCommand

from apps.models import Order, OrderItem, User, Product

# order, orderitem, cart, cartitem, users, product, category

class Command(BaseCommand):
    help = "Bu komanda malumot qoshish uchun "
    model_list = {'orders', 'orderitems'}

    def add_arguments(self, parser):
        parser.add_argument('--orders', type=int, )
        parser.add_argument('--orderitems', type=int)

    def _generate_orders(self, number: int):
        for _ in range(number):
            random_user = User.objects.order_by('?').first()
            Order.objects.create(user=random_user, total_amount=0)
        self.stdout.write(self.style.SUCCESS(f"Order generated - {number}"))

    def _generate_orderitems(self, number: int):
        for _ in range(number):
            random_order = Order.objects.order_by('?').first()
            random_product = Product.objects.order_by('?').first()
            OrderItem.objects.create(
                order=random_order,
                product=random_product,
                quantity=random.randint(1, 10),
                price=random.randint(10, 100) * 1000,
            )

        self.stdout.write(self.style.SUCCESS(f"Order Items generated - {number}"))

    def handle(self, *args, **kwargs):
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        generated_item_names = set(kwargs).intersection(self.model_list)

        for _name in generated_item_names:
            getattr(self, f"_generate_{_name}")(kwargs[_name])

        # order_number = kwargs.get('orders')
        # order_item_number = kwargs.get('orderitems')
        # if order_number:
        #     self._generate_orders(order_number)
        #
        # if order_item_number:
        #     self._generate_orderitems(order_item_number)

        # category_list = []
        # for _ in range(10):
        #     new_category = Category.objects.create(
        #         name=faker.text(max_nb_chars=25)
        #     )
        #     category_list.append(new_category)
        #
        # for _ in range(count):
        #     Post.objects.create(
        #         userId=random.randint(5, 100),
        #         title=faker.paragraph(nb_sentences=2),
        #         category=random.choice(category_list),
        #         type=random.choice(Post.Type.choices)[0],
        #         body=faker.paragraph(nb_sentences=10)
        #     )
        self.stdout.write(self.style.SUCCESS(f"Qo'shildi"))
