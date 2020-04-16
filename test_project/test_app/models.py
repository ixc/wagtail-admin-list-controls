from django.db import models


class TestModel(models.Model):
    char_field = models.CharField(max_length=200, blank=True)

