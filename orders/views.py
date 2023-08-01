from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from orders.models import Order
from django.views.generic.edit import CreateView, UpdateView
import random,string
from django.views.generic import ListView, DetailView
from inventory.models import Inventory
from .forms import MarkCancelledForm, MarkReceivedForm, OrderForm, OrderSpecificForm

def generate_random(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )

class Orders(ListView):
    model = Order
    template_name="orders/orders.html"


def CreateOrder(request):
    context={}
    
    form = OrderForm(request.POST or None)
       
    if form.is_valid():
        quantity = int(request.POST.get('quantity'))
        item_to_be_ordered = request.POST.get('item')
        item_name_to_be_ordered = Inventory.objects.filter(id=item_to_be_ordered).values_list('name', flat=True)[0]
        item_cost = int(Inventory.objects.filter(name=item_name_to_be_ordered).values_list('cost', flat=True)[0])
        bill = item_cost*quantity
        item_to_be_ordered = request.POST.get('item')
        
        
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
        return HttpResponseRedirect(reverse("orders"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"orders/order.html",context)



class ReceivedList(ListView):
    model = Order
    template_name="orders/received.html"

class CancelledList(ListView):
    model = Order
    template_name="orders/cancelled.html"

def OrderSpecific(request,id):

    context={}
    
    form = OrderSpecificForm(request.POST or None)
       
    if form.is_valid():
        quantity = int(request.POST.get('quantity'))
        item_name_to_be_ordered = Inventory.objects.filter(id=id).values_list('name', flat=True)[0]
        item_cost = int(Inventory.objects.filter(name=item_name_to_be_ordered).values_list('cost', flat=True)[0])
        bill = item_cost*quantity
        form.instance.item_id = str(id)
        
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
        return HttpResponseRedirect(reverse("orders"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"orders/order-specific.html",context)

def MarkReceived(request,id):
    context={}
    
    form = MarkReceivedForm(request.POST or None)
       
    if form.is_valid():
        
        
        item = Order.objects.get(id=id)
        #one way of updating db entry
        form.instance.item_id = item.item_id
        form.instance.name = item.name
        form.instance.quantity = item.quantity
        
        item_in_inventory = Inventory.objects.get(id=item.item_id)
        item_in_inventory.quantity+= item.quantity
        item_in_inventory.save()
        
        instance = form.save(commit=False)
        instance.id = str(id)
        instance.cost = item.cost
        instance.orderdttm = item.orderdttm
        instance.is_received = True
        
        instance.save()
        return HttpResponseRedirect(reverse("orders"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"orders/receiveconfirm.html",context)

def MarkCancelled(request,id):
    context={}
    
    form = MarkCancelledForm(request.POST or None)
       
    if form.is_valid():
        
        
        item = Order.objects.get(id=id)

        form.instance.item_id = item.item_id
        form.instance.name = item.name
        form.instance.quantity = item.quantity
        
        instance = form.save(commit=False)
        instance.id = str(id)
        instance.cost = item.cost
        instance.orderdttm = item.orderdttm
        instance.is_cancel = True
        instance.save()
        return HttpResponseRedirect(reverse("orders"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"orders/cancelconfirm.html",context)