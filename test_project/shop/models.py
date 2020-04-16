from django.db import models


class Product(models.Model):
    BREAD = 'bread'
    CAKE = 'cake'
    DRINK = 'drink'

    name = models.CharField(blank=True, max_length=1000)
    items_available = models.IntegerField(blank=True, null=True)
    product_type = models.CharField(
        default=BREAD,
        choices=(
            (BREAD, 'Bread'),
            (CAKE, 'Cake'),
            (DRINK, 'Drink'),
        ),
        max_length=1000,
    )
    is_featured = models.BooleanField(default=False)
