# models.py
from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    origin = models.CharField(max_length=100, blank=True, null=True)
    lifespan = models.CharField(max_length=100, blank=True, null=True)
    ideal_conditions = models.TextField(blank=True, null=True)
    home_remedies = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # New fields
    binomial_name = models.CharField(max_length=100, blank=True, null=True)
    taxon = models.CharField(max_length=50, blank=True, null=True)
    companions = models.TextField(blank=True, null=True)
    sun_requirements = models.CharField(max_length=100, blank=True, null=True)
    growing_degree_days = models.CharField(max_length=100, blank=True, null=True)
    sowing_method = models.TextField(blank=True, null=True)
    spread = models.CharField(max_length=100, blank=True, null=True)
    row_spacing = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
