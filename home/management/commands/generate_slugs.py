from django.core.management.base import BaseCommand
from django.utils.text import slugify
from home.models import Products, Categories

class Command(BaseCommand):
    help = 'Generate slugs for Categories and Products where they are missing'

    def handle(self, *args, **kwargs):
        # Update Categories
        for category in Categories.objects.all():
            if not category.slug:
                category.slug = slugify(category.name)
                counter = 2
                base_slug = category.slug
                while Categories.objects.filter(slug=category.slug).exclude(pk=category.pk).exists():
                    category.slug = f"{base_slug}-{counter}"
                    counter += 1
                category.save()
                self.stdout.write(self.style.SUCCESS(f'Updated category: {category.name} -> {category.slug}'))

        # Update Products
        for product in Products.objects.all():
            if not product.slug:
                product.slug = slugify(product.name)
                counter = 1
                base_slug = product.slug
                while Products.objects.filter(slug=product.slug).exclude(pk=product.pk).exists():
                    product.slug = f"{base_slug}-{counter}"
                    counter += 1
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Updated product: {product.name} -> {product.slug}'))

        self.stdout.write(self.style.SUCCESS('Slug generation completed!'))