from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView
from inventory.models import Inventory
from transactions.forms import SellForm, SellSpecificForm
from .models import Transactions
# Create your views here.
import random,string

def generate_random(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )

class Transactions(ListView):
    model = Transactions
    template_name="transactions/transactions.html"

    

def CreateTransaction(request):
    context={}
    
    form = SellForm(request.POST or None)

    if form.is_valid():
        quantity = int(request.POST.get('quantity'))
        item_to_be_ordered = request.POST.get('item')
        item_name_to_be_ordered = Inventory.objects.filter(id=item_to_be_ordered).values_list('name', flat=True)[0]
        item_cost = int(Inventory.objects.filter(name=item_name_to_be_ordered).values_list('selling_price', flat=True)[0])
        bill = item_cost*quantity
        item_to_be_ordered = request.POST.get('item')
        in_stock = Inventory.objects.filter(id=item_to_be_ordered).values_list('quantity',flat=True)[0]
        # print(item_name_to_be_ordered)
        form.instance.selling_price = item_cost*quantity
        if in_stock<quantity:
            return HttpResponse("Maximum quantity available: "+str(in_stock))
        item = Inventory.objects.get(id=item_to_be_ordered)
        item.quantity = in_stock-quantity
        item.quantity_sold = quantity
        item.profit_earned = item.quantity_sold*(item.selling_price-item.cost)
        item.save()
        
        instance = form.save(commit=False)
        instance.cost = bill

        while True:
            new_name = generate_random(8)
            duplicate_name = Inventory.objects.filter(name=new_name).values_list(flat=True)
            
            if len(duplicate_name)==0:
                instance.name = new_name
                break
        
        while True:
            new_id = random.randint(1,10**7)
            duplicate_id = Inventory.objects.filter(id=new_id).values_list(flat=True)
            if len(duplicate_id)==0:
                instance.id = new_id
                break

        instance.save()
        return HttpResponseRedirect(reverse("transactions"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"transactions/sell.html",context)

def TransactSpecific(request,id):
    context={}
    
    form = SellSpecificForm(request.POST or None)
       
    if form.is_valid():
        quantity = int(request.POST.get('quantity'))
        item_name_to_be_ordered = Inventory.objects.filter(id=id).values_list('name', flat=True)[0]
        item_cost = int(Inventory.objects.filter(name=item_name_to_be_ordered).values_list('selling_price', flat=True)[0])
        bill = item_cost*quantity
        form.instance.item_id = str(id)
        in_stock = Inventory.objects.filter(id=id).values_list('quantity',flat=True)[0]
        if in_stock<quantity:
            return HttpResponse("Maximum quantity available: "+str(in_stock))
        item = Inventory.objects.get(id=id)
        item.quantity = in_stock-quantity
        item.quantity_sold = quantity
        
        item.profit_earned = item.quantity_sold*(item.selling_price-item.cost)
        item.save()
        instance = form.save(commit=False)
        instance.selling_price = bill
        
        while True:
            new_name = generate_random(8)
            duplicate_name = Inventory.objects.filter(name=new_name).values_list(flat=True)
            
            if len(duplicate_name)==0:
                instance.name = new_name
                break
        
        while True:
            new_id = random.randint(1,10**7)
            duplicate_id = Inventory.objects.filter(id=new_id).values_list(flat=True)
            if len(duplicate_id)==0:
                instance.id = new_id
                break
    
        instance.save()
        return HttpResponseRedirect(reverse("transactions"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"transactions/sell-specific.html",context)