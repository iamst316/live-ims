from django.shortcuts import render
import json
# Create your views here.

def ManagementHome(request):

    f = open('media/management.json')
    data = json.load(f)
    f.close()
    jsonData = json.dumps(data)
    # print(data)

    return render(request,'management/home.html',{
        'data': data,
        'jsonData' : jsonData
    })