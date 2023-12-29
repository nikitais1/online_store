from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'category_name': 'a', 'description': 'aaa'},
            {'category_name': 'b', 'description': 'bbb'},
            {'category_name': 'c', 'description': 'ccc'}
        ]

        category_for_create = []
        for category in category_list:
            category_for_create.append(
                Category(**category)
            )
        Category.objects.all().delete()
        Category.objects.bulk_create(category_for_create)

