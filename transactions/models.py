from django.db import models
from inventory.models import Inventory
# Create your models here.

class Transactions(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    item = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    selling_price = models.IntegerField()
    transactiondttm = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

