from django.shortcuts import render
from django.http import HttpResponse

from home.models import Contact

def index(request):
    return render(request, 'index.html')

def contact_us(request):
    context={}
    if request.method == "POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message")

        obj = Contact(name=name, email=em, subject=sub, message=msz)
        obj.save()
        context['message']=f" Dear {name}, Thanks for the information"


    return render(request, 'contact.html', context)

def about(request):
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')
