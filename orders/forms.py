from django import forms
from .models import Order
  
  
# creating a form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = ["id","name","item","quantity"]
        fields = [
            "item","quantity"]
class OrderSpecificForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["quantity"]
        
class MarkReceivedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

class MarkCancelledForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []