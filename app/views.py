from django.shortcuts import render,redirect,HttpResponse # type: ignore
from app.models import pet,cart,order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail
# Create your views here.
def index(request):
    context ={}
    data=pet.objects.all()
    context['pets'] = data
    return render(request,"index.html",context)

def details(request,rid):
    context={}
    data=pet.objects.get(id = rid)
    context['pet']=data
    return render(request,'details.html',context)

def registration(request):
    if request.method == "GET":
        return render(request,'registration.html')
    else:
        u=request.POST['username']
        if User.objects.filter(username = u).exists():
            messages.warning(request,"Username already regsitered!!  please enter a diffrent username for registration")
            return render(request,'login.html')
        else:
            e=request.POST['email']
            p=request.POST['password']
            cp=request.POST["cpassword"]
            if p != cp:
                messages.warning('"password and confirm password must same"')
                return render(request,'registration.html')
            else:
                u=User.objects.create(username=u,email=e)
                u.set_password(p)
                u.save()
                messages.warning(request,'Registration successfully , Please login')
                return redirect('/login')
    

def userlogin(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u=request.POST['username']
        p=request.POST['password']
        us=authenticate(username=u,password=p)
        if us == None:
         messages.warning(request,'username and password not matched please try again')
         return redirect('/login')
        else:
            login(request,us)
            messages.success(request,'Login succesfully !!!')
            return redirect('/')

def userlogout(request):
    logout(request)
    messages.warning(request,'User logged out Successfully!!')
    return redirect("/")

def addtocart(request,petid):
    userid=request.user.id
    context={}
    if userid is None:
        messages.warning(request,'please login so as to add the pet in your cart')
        return render(request,'login.html',context)
    else:
        users=User.objects.filter(id = userid)
        pets=pet.objects.filter(id = petid)
        carts=cart.objects.create(pid = pets[0],uid = users[0])
        carts.save()
        messages.success(request,'pet added to cart!!')
        return redirect('/')


def removepet(request,cid):
    data = cart.objects.filter(id = cid)
    data.delete()
    messages.success(request,"pet remove from mycart")
    return redirect('/showcart')

def showusercart(request):
    user = request.user
    carts = cart.objects.filter(uid = user.id)
    totalbill=0
    for c in carts:
        totalbill += c.pid.price * c.quantity
    count = len(carts)
    contex = {
        'cart':carts,
        'total':totalbill,
        'c':count
    }

    # contex['cart'] = carts
    # contex['total'] = totalbill
    # contex['c'] = count
    return render(request,'showcart.html',contex)


def updatecart(request,opr,cartid):
    carts=cart.objects.filter(id=cartid)
    if opr=='1':
        carts.update(quantity = carts[0].quantity + 1)
    else:
        if carts[0].quantity > 1:
            carts.update(quantity = carts[0].quantity - 1)
        else:
            carts.update(quantity = 1)


    return redirect('/showcart')

def searchbytype(request,pet_type):
    petlist = pet.objects.filter(type = pet_type)
    context={'pets':petlist}
    return render(request,'index.html',context)


def pricerange(request):
   min = request.GET['min']
   max = request.GET['max']
   c1 = Q(price__gte = min)
   c2 = Q(price__lte = max)
   petlist = pet.objects.filter(c1 & c2)
   context={'pets':petlist}
   return render(request,'index.html',context)

def sortrange(request,ord):
    col=''
    if ord == 'asc':
     col='price'
    else:
        col= '-price'
    petlist = pet.objects.all().order_by(col)
    context={'pets':petlist}
    return render(request,'index.html',context)


def confirmorder(request):
    context ={}
    # user = request.user
    # data = cart.objects.filter(uid = user.id)
    # context['cart'] = data
    # return render(request,"showcart.html",context)
    user = request.user
    carts = cart.objects.filter(uid = user.id)
    totalbill=0
    for c in carts:
        totalbill += c.pid.price * c.quantity
    count = len(carts)
    context = {
        'cart':carts,
        'total':totalbill,
        'c':count
    }
    return render(request,"confirmorder.html",context)

  

def makepayment(request):
    user = request.user
    usercart = cart.objects.filter(uid = user.id)
    totalbill = 0
    for c in usercart:
        totalbill += c.pid.price * c.quantity
    client = razorpay.Client(auth=("rzp_test_tIqAd7OXqu2xWS", "Nt4xEdPZ2llmou7xC55FfCmq"))
    data = { "amount": totalbill*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={'data':payment}
    return render(request,'pay.html',context)

def confirmpayment(request):
    user = request.user
    old = random.randrange(10000,99999)
    # print(user.id,user.username)
    my_cart = cart.objects.filter(uid = user.id)

    for cartt in my_cart:
        Order = order.objects.create(order_id = old,uid = cartt.uid,pid = cartt.pid,quantity = cartt.quantity)
        Order.save()

    my_cart.delete()

    msgbody = 'Your order is placed succesfully.'
    msg='your order id'+str(order.order_id)

    useremail = user.email

    send_mail(
    msgbody,
    msg,
    "dharmeshhh011@gmail.com",
    [useremail],
    fail_silently=False,
)
    return redirect('/')

def useraddress(request):
    return render(request,'address.html')



# views

def exp_pets(request):
    pets = pet.objects.filter(price__gt=5000)  # Pets with price greater than 5000
    return render(request, 'index.html', {'pets': pets})