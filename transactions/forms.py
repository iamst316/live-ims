from django import forms
from .models import Transactions


class SellForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ["item","quantity"]
        
class SellSpecificForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ["quantity"]