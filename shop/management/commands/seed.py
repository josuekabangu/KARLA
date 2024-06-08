from django.core.management.base import BaseCommand
from shop.models import Category, Product
import random
from decimal import Decimal
from faker import Faker

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def __init__(self):
        super().__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self._create_categories()
        self._create_products()
        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))

    def _create_categories(self):
        categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Toys']
        for category in categories:
            Category.objects.get_or_create(name=category)
        self.stdout.write(self.style.SUCCESS('Categories created'))

    def _create_products(self):
        categories = Category.objects.all()
        for _ in range(50):
            category = random.choice(categories)
            product_name = self.fake.unique.word().capitalize()
            price = Decimal(random.uniform(10.0, 500.0)).quantize(Decimal('0.01'))
            stock = random.randint(1, 100)
            description = self.fake.text(max_nb_chars=200)
            Product.objects.create(
                name=product_name,
                description=description,
                price=price,
                stock=stock,
                category=category
            )
        self.stdout.write(self.style.SUCCESS('Products created'))
