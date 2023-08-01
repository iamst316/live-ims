from django.db import models
from django.urls import reverse

# Create your models here.


class Inventory(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    iin = models.CharField(max_length=8, blank=True, unique=True)
    cost = models.IntegerField()
    category = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField()
    quantity_sold = models.IntegerField(default=0)
    selling_price = models.PositiveIntegerField()
    profit_earned = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)
    

    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse("item-details", kwargs={"pk": self.pk})
    
