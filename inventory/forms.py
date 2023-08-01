from .models import Inventory
from django import forms

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "name","cost","quantity","selling_price"]
        
class AddSpecificItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "cost","quantity","selling_price"]