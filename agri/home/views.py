from ssl import AlertDescription
from django.shortcuts import render, HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from home.models import Test
from .forms import TestForm
from json import dumps
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import smtplib
import random
# Import the email modules we'll need
from email.message import EmailMessage
# Create your views here.
val1=None
val2=None
val3=None

def index(request):
    return render(request,"home.html")
    
def contact(request):
    return render(request,"contact.html")

def searching(request):
      if request.method == 'POST':
        search_id = request.POST.get('search', '')
      url1="https://www.apollopharmacy.in/search-medicines/"+search_id
      url2="https://pharmeasy.in/search/all?name="+search_id
      r1=requests.get(url1)
      r2=requests.get(url2)

      htmlContent1=r1.content
      htmlContent2=r2.content
      soup1=BeautifulSoup(htmlContent1,'html.parser')
      soup2=BeautifulSoup(htmlContent2,'html.parser')

      result1=soup1.find_all("p",class_="ProductCard_productName__2LhTY")
      result2=soup2.find_all("h1",class_="ooufh")
     
      names1=[]
      names2=[]
      final_names=[]
      for name in result1:
           names1.append(name.text)
      for name in result2:
           names2.append(name.text)

      final_names=names1+names2
            
      mylist=zip(names1,names2)
      n1=len(names1)
      n2=len(names2)
      n3=len(final_names)

      global val1
      def val1():
        return n1
      
      global val2
      def val2():
        return n2

      global val3
      def val3():
        return n3
      
      context={
               'v1':final_names,
               'v2':mylist
              }         
      return render(request,"results.html",context)
 
def order(request):
      return render(request,"order.html")

def cart(request):
  if request.user.is_anonymous:
        return redirect("/login")
  else:
    if request.method == 'POST':
      product=request.POST.get("product",'')

    cart=request.session.get('cart')
    if cart:
        quantity=cart.get(product)
        if quantity:
            cart[product]=quantity+1
        else:
            cart[product]=1
    else:
        cart={}
        cart[product]=1
    
    request.session['cart']=cart
   # print('cart is ',request.session['cart'])
    context={
        'v4':request.session['cart'].items()
    }
    v5=request.session['cart']
    return render(request,"cart.html",context)

def signup(request):
      if request.method=="POST":
          username=request.POST.get('username')
          mobile=request.POST.get('mobile')
          password=request.POST.get('password')
          global otpn
          otpn=random.randint(1000,9000)
          account_sid = 'AC816136a1a9f233920377dd89348899e3' 
          auth_token = 'b211d7195750b36efdb9e02fc2e1d79b' 
          client = Client(account_sid, auth_token) 
 
          message = client.messages.create(  
                              messaging_service_sid='MG48304d20ff9ea4ba16c2cef1abcd909f', 
                              body=f'Your otp is {otpn}',      
                              to='+919822976556' 
                          ) 
 
          print("message",message.sid)
          global user
          user=User.objects.create_user(username=username,password=password)
        #   user.save()
          return render(request,"otp.html")
      return render(request,"signup.html")

def loginuser(request):
    if request.method=="POST":
       username=request.POST.get("username")
       password=request.POST.get("password")

       user= authenticate(username=username,password=password)
       
       if user is not None:
           login(request,user)
           messages.success(request,"Logged in Successfully")
           return redirect("/")
       else:
           messages.error(request,"Invalid Credentials")
           return render(request,"login.html")
    return render(request,"login.html")

def logoutuser(request):
    logout(request)
    return redirect('/')
    
def image(request):
     n1=val1()
     if request.method == 'POST':
       products=request.POST.get("products",'')
       product_id=request.POST.get("product_id",'')

     if int(product_id)<=n1:
        url1="https://www.apollopharmacy.in/search-medicines/"+products
        r1=requests.get(url1)
        htmlContent1=r1.content
        soup1=BeautifulSoup(htmlContent1,'html.parser')
        result=soup1.find("div",class_="ProductCard_bigAvatar__2D8AB").contents[0]['src']
        print(result)
        s3="https://newassets.apollo247.com/pub/media/thumbnail/apollo24logo.png"
        if result==s3:
            f_res=s3
        else:
         s1=result[0:57]
         word='jpeg'
         if word in result:
            s2=result[-17:]
         else:
            s2=result[-16:]
         f_res=s1+s2
         
     else:
         new_pro=products.replace(" ","+")
         url1="https://pharmeasy.in/search/all?name="+new_pro
         print(new_pro)
         print(url1)
         r1=requests.get(url1)
         htmlContent1=r1.content
         soup1=BeautifulSoup(htmlContent1,'html.parser')
         check=soup1.find_all("h1",class_="ooufh")
         a=0
         for i in check:
             if i.text==products:
                 break
             else:
                 a=a+1
         result=soup1.find_all("a",class_="_2tdEn _1pXi6 _3o0NT _1NxW8 iJm6I")
         result1=result[a].get('href')
         url2="https://pharmeasy.in"+result1
         print(url2)
         def handle(url):
             try:
                  r2=requests.get(url)
                  htmlContent2=r2.content
                  soup2=BeautifulSoup(htmlContent2,'html.parser')
                  f_res1=soup2.find("img",class_="LCPImage_imgContainer__1a-oJ").get('src')
                  print(f_res1)
             except AttributeError as e:
                 return None
             return f_res1
         f_res=handle(url2)
         print(f_res)
     context={
           'v3':f_res
         }

     return render(request,"image.html",context)


def uploadImage(request):
    if request.method=="POST":
        x=request.POST.get('cars')
        y=request.POST.get('season')
        z=request.POST.get('rainfall')
        print(x,y,z)
    return HttpResponse("hi")

def calc(request):
    list_quantity=[]
    list_prices1=[]
    list_prices2=[]
    s1=""
    s2=""
    total2=0
    total1=0
    if request.method == "POST":
      for k,v in request.session['cart'].items():
          var=request.POST.get(k)
          print(var)
     
   # print(request.session['cart'].items())
    for k,v in request.session['cart'].items():
        url1="https://www.apollopharmacy.in/search-medicines/"+k
        r1=requests.get(url1)
        htmlContent1=r1.content
        soup1=BeautifulSoup(htmlContent1,'html.parser')
        result1=soup1.find("div",class_="ProductCard_priceGroup__Xriou").text
        #print(result)
        s1=result1[result1.index(")")+2:-1]
        #print(float(s1))
        list_prices1.append(float(s1))
        list_quantity.append(v)
        #print(s1)
        url2="https://pharmeasy.in/search/all?name="+k
        r2=requests.get(url2)
        htmlContent2=r2.content
        soup2=BeautifulSoup(htmlContent2,'html.parser')
        result2=soup2.find("div",class_="_1_yM9").text
        #print(result2)
        s2=result2[result2.index("₹")+1:-2]
        #print(float(s2))
        list_prices2.append(float(s2))
    for i in range(len(list_quantity)):
        total1=total1+(list_prices1[i]*float(list_quantity[i]))
        total2=total2+(list_prices2[i]*float(list_quantity[i]))
    print(total1)
    print(total2)
       # list_items.append(k)
       # list_quantity.append(v)
    mylist = zip(list_prices1, list_prices2)
    context={
        'v1':float("{:.2f}".format(total1)),
        'v2':float("{:.2f}".format(total2)),
        'v4':request.session['cart'].items(),
        'v5': mylist
    }    
    #order
    return render(request,"total.html",context)

def add(request):
    if request.method == "POST":
     #  var =request.POST.get('item')
       for k,v in request.session['cart'].items():
            var=request.POST.get(k)
     #       if var == k:
      #      request.session['cart'][k] +=1
       #     break
    context={
        'v4':request.session['cart'].items()
    }
    print(request.session['cart'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
def cart_view(request):
     context={
        'v4':request.session.items()
     }
     return render(request,"cart_view.html",context)

def exit(request):
     print("hello")
    #  a=Test.objects.create(image1=None,sub2=99)
     a=Test(image1=None,sub2=6)
     
     a.save()
     
 
     account_sid = 'AC816136a1a9f233920377dd89348899e3' 
     auth_token = 'b211d7195750b36efdb9e02fc2e1d79b' 
     client = Client(account_sid, auth_token) 
 
     message = client.messages.create(  
                              messaging_service_sid='MG48304d20ff9ea4ba16c2cef1abcd909f', 
                              body='noob',      
                              to='+919822976556' 
                          ) 
 
     print("message",message.sid)
    
     return redirect("/")


def otp(request):
    if request.method=="POST":
       if otpn == int(request.POST.get('otp')):
          user.save()
       else:
        return render(request,"signup.html")
    return render(request,"home.html")