from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from home.models import Contact, Dish, Category, Profile, Order
from django.contrib.auth import login, authenticate, logout
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def index(request):
    context ={}
    cats = Category.objects.all().order_by('name')
    context['categories'] = cats
    # print()
    dishes = []
    for cat in cats:
        dishes.append({
            'cat_id':cat.id,
            'cat_name':cat.name,
            'cat_img':cat.image,
            'items':list(cat.dish_set.all().values())
        })
    context['menu'] = dishes
    return render(request,'index.html', context)

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
    context={}
    if request.method=="POST":
        #fetch data from html form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')
        check = User.objects.filter(username=email)
        if len(check)==0:
            #Save data to both tables
            usr = User.objects.create_user(email, email, password)
            usr.first_name = name
            usr.save()

            profile = Profile(user=usr, contact_number = contact)
            profile.save()
            context['status'] = f"User {name} Registered Successfully!"
        else:
            context['error'] = f"A User with this email already exists"

    return render(request,'register.html', context)

def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})
    

def signin(request):
    context={}
    if request.method=="POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email, password=passw)
        if check_user:
            login(request, check_user)
            return HttpResponseRedirect('/dashboard/')
            # if check_user.is_superuser or check_user.is_staff:
            #     return HttpResponseRedirect('/admin')
            # return HttpResponseRedirect('/dashboard')
        else:
            context.update({'message':'Invalid Login Details!','class':'alert-danger'})
    return render(request, 'login.html', context)

def all_dishes(request):
    context={}
    dishes = Dish.objects.all()
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name 

    context['dishes'] = dishes
    return render(request,'all_dishes.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def single_dish(request, id):
    context={}
    dish = get_object_or_404(Dish, id=id)

    if request.user.is_authenticated:
        cust = get_object_or_404(Profile, user__id = request.user.id)
        order = Order(customer=cust, item=dish)
        order.save()
        inv = f'INV0000-{order.id}'

        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':dish.discounted_price,
            'item_name':dish.name,
            'user_id':request.user.id,
            'invoice':inv,
            'notify_url':'http://{}{}'.format(settings.HOST, reverse('paypal-ipn')),
            'return_url':'http://{}{}'.format(settings.HOST,reverse('payment_done')),
            'cancel_url':'http://{}{}'.format(settings.HOST,reverse('payment_cancel')),
        }

        order.invoice_id = inv 
        order.save()
        request.session['order_id'] = order.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({'dish':dish, 'form':form})

    return render(request,'dish.html', context)