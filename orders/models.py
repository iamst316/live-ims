from django.db import models
from django.urls import reverse
from inventory.models import Inventory

# Create your models here.

class Order(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    item = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.PositiveIntegerField()
    orderdttm = models.DateTimeField(auto_now_add = True)
    is_received = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return self.name
    
    