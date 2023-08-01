from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from inventory.forms import AddItemForm
import random
import string

from orders.models import Order
from .models import Inventory
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView
from json import dumps


# Create your views here.

def generate_random(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )

def Home(request):
    
    dict={}

    items = Inventory.objects.all().values_list('name',flat=True)[::1]
    # print(items)
    quantList = Inventory.objects.all().values_list('quantity',flat=True)[::1]
    profitList = Inventory.objects.all().values_list('profit_earned',flat=True)[::1]
    costlyArr = Inventory.objects.all().values_list('selling_price',flat=True)[::1]
    costlyArr.sort()
    # costliest= costlyArr[-1]

    # costlyname = Inventory.objects.filter(selling_price=costliest).first()
    # print(costlyname)

    totalProfit = sum(profitList)
    soldArr = Inventory.objects.all().values_list('quantity_sold',flat=True)[::1]
    soldArr.sort()
    
    # print(soldArr)

    # mostSoldNum= soldArr[-1]
    # mostSoldName = Inventory.objects.filter(quantity_sold=mostSoldNum).first()
    items_out_of_stock=Inventory.objects.filter(quantity=0).values_list('name',flat=True)[::1]
    items_oos_length=len(items_out_of_stock)
    
    inv_db = Inventory.objects.all()[::1]
    
    maxProfitable = 0
    maxProfitableName = ""
    for inv in inv_db:
        item_profit = inv.selling_price-inv.cost
        
        if item_profit>maxProfitable:
            maxProfitable = item_profit
            maxProfitableName = inv.name
    
    

    
    #chart-stuff
    dict['profits'] = profitList
    dict['items'] = items
    dict['quantity'] = quantList
    dataJSON = dumps(dict)
    #chart-stuff ends
    
    return render(request,"pages/home.html",{'data':dataJSON,'totalProfit':totalProfit,
    # 'costliest':costliest,
    # "costlyname":costlyname,
    "items_out_of_stock":items_out_of_stock,
    "items_oos_length":items_oos_length,
    "maxProfitableName":maxProfitableName,
    "maxProfitable":maxProfitable,
    # "mostSoldNum":mostSoldNum,
    # "mostSoldName":mostSoldName
    })

class Items(ListView):
    model = Inventory
    template_name="pages/items.html"

class ItemEditList(ListView):
    model = Inventory
    template_name="pages/edititemlist.html"

class ItemViewList(ListView):
    model = Inventory
    template_name="pages/itemdetailslist.html"


def AddItem(request):
    context={}
    form = AddItemForm(request.POST or None)
    
    if form.is_valid():
        instance = form.save(commit=False)  
    
        while True:
            new_iin = generate_random(8)
            duplicate_iin = Inventory.objects.filter(iin=new_iin).values_list(flat=True)
            # print(duplicate_iin)
            # break
            if len(duplicate_iin)==0:
                instance.iin = new_iin
                break

        while True:
            new_id = random.randint(1,10**7)
            duplicate_id = Inventory.objects.filter(id=new_id).values_list(flat=True)
            # print(duplicate_id)
            # break
            if len(duplicate_id)==0:
                instance.id = new_id
                break

        instance.save()
        return HttpResponseRedirect(reverse("items"))

    else:
        HttpResponse("<h2>Invalid Form Entries</h2>")

    context['form'] = form

    return render(request,"pages/additem.html",context)
    
class ItemDetailsView(DetailView):
    model = Inventory
    template_name = "pages/itemdetails.html"
    # success_url="item/:id"

class EditItemDetailsView(UpdateView):
    model = Inventory
    template_name = "pages/edititem.html"
    fields = ["id","name","iin","cost","quantity","selling_price"]


def ItemSpecificOrders(request,id):
    orders = Order.objects.filter(item_id=id)[::1]
    length = len(orders)
    context={}
    context['length'] = length
    context['orders'] = orders

    return render(request,"pages/item-orders.html",context)

def ItemSpecificReceivedOrders(request,id):
    orders = Order.objects.filter(item_id=id,is_received=1)[::1]
    length = len(orders)
    context={}
    context['length'] = length
    context['orders'] = orders

    return render(request,"pages/items-orders-received.html",context)

def ItemSpecificCancelledOrders(request,id):
    orders = Order.objects.filter(item_id=id,is_cancel=1)[::1]
    length = len(orders)
    context={}
    context['length'] = length
    context['orders'] = orders

    return render(request,"pages/items-orders-cancelled.html",context)
