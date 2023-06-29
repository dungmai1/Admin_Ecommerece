from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collections import OrderedDict
# Create your views here.

import pyrebase
from .form import NameForm,UpdateProduct,UpdateUser,UserForm,AddCategoryForm,EditStatusForm



# Remember the code we copied from Firebase.
#This can be copied by clicking on the settings icon > project settings, then scroll down in your firebase dashboard
config={
    "apiKey": "AIzaSyBcM1YFy485n_eTmG1PalrtQhwUVcpiPgA",
    "authDomain": "fireapp-6d3ed.firebaseapp.com",
    "databaseURL": "https://ecommercelogin-6d3ed-default-rtdb.firebaseio.com",
    "projectId": "ecommercelogin-6d3ed",
    "storageBucket": "fireapp-6d3ed.appspot.com",
    "messagingSenderId": "",
    "appId": "1:1005828844830:android:e93d5d9c76a11f1dc4ad0f",
    "measurementId": ""
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def products(request):
    products_data = database.child('Products').child('Category').get()
    products_key_values = []
    for item in products_data.each():
        products_data1 = products_data = database.child('Products').child('Category').child(item.key()).get()
        for item1 in products_data1.each():
            products_key_values.append({'key': item1.key(), 'value': item1.val()})
    context = {'products_key_values': products_key_values}
    return render(request, 'theme/pages/products.html', context)
def home(request):
    return render(request, 'theme/index.html')
def addnewproduct(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["ProductName"]
            category = form.cleaned_data["Category"]
            price = form.cleaned_data["Price"]
            price = int(price)
            image_url = form.cleaned_data["ImageProduct"]
            description = form.cleaned_data["Description"]
            ImageDetail1 = form.cleaned_data["ImageDetail1"]
            ImageDetail2 = form.cleaned_data["ImageDetail2"]
            ImageDetail3 = form.cleaned_data["ImageDetail3"]
            ImageDetail4 = form.cleaned_data["ImageDetail4"]
            new_product = {
                "ProductName": product_name,
                "Price": price,
                "Category":category,
                "ImageProduct": image_url,
                "ProductDetail": {
                    "Description": description,
                    "ImageDetail1": ImageDetail1,
                    "ImageDetail2": ImageDetail2,
                    "ImageDetail3": ImageDetail3,
                    "ImageDetail4": ImageDetail4
                }               
            }
            database.child('Products').child('Category').child(category).push(new_product)
            return HttpResponseRedirect("/products/")
    else:
        form = NameForm()
    return render(request, "theme/pages/addproducts.html", {"form": form})
    
def deleteproduct(request,id,category_value):
    database.child("Products").child("Category").child(category_value).child(str(id)).remove()
    return HttpResponseRedirect("/products/")

def updateproducts(request,id,Category):
    product = None
    key = None
    if request.method == "POST":
        form = UpdateProduct(request.POST)
        if form.is_valid():    
            product_name = form.cleaned_data["ProductName"]
            price = form.cleaned_data["Price"]
            price = int(price)
            image_url = form.cleaned_data["ImageProduct"]
            description = form.cleaned_data["Description"]
            ImageDetail1 = form.cleaned_data["ImageDetail1"]
            ImageDetail2 = form.cleaned_data["ImageDetail2"]
            ImageDetail3 = form.cleaned_data["ImageDetail3"]
            ImageDetail4 = form.cleaned_data["ImageDetail4"]
            
            product = database.child('Products').child('Category').child(Category).child(id).get().val()
            # Update the product data
            product = {
                "ProductName": product_name,
                "Price": price,
                "Category":Category,
                "ImageProduct": image_url,
                "ProductDetail": {
                    "Description": description,
                    "ImageDetail1": ImageDetail1,
                    "ImageDetail2": ImageDetail2,
                    "ImageDetail3": ImageDetail3,
                    "ImageDetail4": ImageDetail4
                }
            }
            database.child('Products').child('Category').child(Category).child(id).update(product)
            
            return HttpResponseRedirect("/products/")
        return HttpResponse('Form Error')
    else:
        form = UpdateProduct()
        key = database.child('Products').child('Category').child(str(id)).get()
        product = database.child('Products').child('Category').child(Category).child(str(id)).get().val()

    return render(request, "theme/pages/updateproducts.html", {"form": form, "product": product, "key": key})    
      
def users(request):
    user_data = database.child('Users').get()
    user_data_key = []
    for item in user_data.each():
        user_data_key.append({'key': item.key(), 'value': item.val()})
    context = {'user_data_key': user_data_key}
    return render(request, 'theme/pages/users.html', context) 
def addnewuser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            lastname = form.cleaned_data["LastName"]
            firstname = form.cleaned_data["FirstName"]
            phoneNumber = form.cleaned_data["PhoneNumber"]
            phoneNumber = int(phoneNumber)
            password = form.cleaned_data["Password"]
            user = {
                "phoneNumber": phoneNumber,        
                "lastName": lastname,
                "firstName": firstname,
                "password": password,
            }
            database.child("Users").push(user)
            return HttpResponseRedirect("/users/")
    else:
        form = UserForm()
    return render(request, "theme/pages/addnewuser.html", {"form": form})
def AddressUser(request, id):
    try:
        address_data = database.child('Address').child(id).get().val()
        if address_data:
            address_key_values = []
            for key, value in address_data.items():
                address_key_values.append({'key': key, 'value': value})
            context = {'address_key_values': address_key_values}
            return render(request, 'theme/pages/AddressUser.html', context)
        else:
            # Address with the given ID does not exist
            return render(request, 'theme/pages/AddressUserFound.html')
    except AttributeError:
        # Address with the given ID does not exist
        return render(request, 'theme/pages/AddressUserFound.html')

def order(request):
    order_key = database.child('Order').get()
    order_dt = []
    count_processing = 0
    count_shipping = 0
    count_delivered = 0
    count_canceled = 0
    for item in order_key.each():
        order_data = database.child('Order').child(item.key()).get()
        for item1 in order_data.each():
            status = item1.val()["Status"]
            if status == "Processing":
                count_processing += 1
            if status == "Shipping":
                count_shipping += 1
            if status == "Delivered":
                count_delivered += 1
            if status == "Canceled":
                count_canceled += 1                
    context = {
        'count_processing': count_processing,
        'count_shipping': count_shipping,
        'count_delivered': count_delivered,
        'count_canceled': count_canceled,
    }
    return render(request, 'theme/pages/order.html', context)

def processing(request):
    order_key = database.child('Order').get()
    order_dt = []
    for item in order_key.each():
        order_data = database.child('Order').child(item.key()).get()
        for item1 in order_data.each():
            status = item1.val()["Status"]
            if(status == "Processing"):
                order_dt.append({'key': item1.key(), 'value': item1.val()
                    ,'user':item.key()})
    context ={
        'order_dt': order_dt,
    }
    return render(request,'theme/pages/processing.html',context)

def viewOrderProcessing(request,id,iduser):
    order_processing = database.child('Order').child(iduser).child(id).child('Products').get()
    order_values = []
    for item in order_processing.each():
        order_values.append({'key': item.key(), 'value': item.val()})
    context ={
        'order_values': order_values
    }
    return render(request,'theme/pages/viewOrderProcessing.html',context)

def shipping(request):
    order_key = database.child('Order').get()
    order_dt = []
    for item in order_key.each():
        order_data = database.child('Order').child(item.key()).get()
        for item1 in order_data.each():
            status = item1.val()["Status"]
            if(status == "Shipping"):
                order_dt.append({'key': item1.key(), 'value': item1.val()
                    ,'user':item.key()})
    context ={
        'order_dt': order_dt,
    }
    return render(request,'theme/pages/shipping.html',context)

def delivered(request):
    order_key = database.child('Order').get()
    order_dt = []
    for item in order_key.each():
        order_data = database.child('Order').child(item.key()).get()
        for item1 in order_data.each():
            status = item1.val()["Status"]
            if(status == "Delivered"):
                order_dt.append({'key': item1.key(), 'value': item1.val()
                    ,'user':item.key()})
    context ={
        'order_dt': order_dt,
    }
    return render(request,'theme/pages/delivered.html',context)

def canceled(request):
    order_key = database.child('Order').get()
    order_dt = []
    for item in order_key.each():
        order_data = database.child('Order').child(item.key()).get()
        for item1 in order_data.each():
            status = item1.val()["Status"]
            if(status == "Canceled"):
                order_dt.append({'key': item1.key(), 'value': item1.val()
                    ,'user':item.key()})
    context ={
        'order_dt': order_dt,
    }
    return render(request,'theme/pages/cancel.html',context)

def signin(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Retrieve admin data from the database
        admin = database.child('Admin').get().val()
        
        # Check if the entered email matches the stored email
        if email == admin.get('email'):
            # Check if the entered password matches the stored password
            if password == admin.get('password'):
                # Authentication successful, redirect to a logged-in page
                return render(request,'theme/index.html')
        # Authentication failed, display an error message
        error_message = "Invalid credentials. Please try again."
        return render(request, 'theme/pages/sign-in.html', {'error_message': error_message})
    return render(request, 'theme/pages/sign-in.html')

def Category(request):
    category_data = database.child('Category').get()
    category_values = []
    for item in category_data.each():
        category_values.append({'key': item.key(), 'value': item.val()})
    context = {'category_values': category_values}
    return render(request, 'theme/pages/category.html',context)

def addCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            CategoryName = form.cleaned_data["CategoryName"]
            Description = form.cleaned_data["Description"]
            ImageCategory = form.cleaned_data["ImageCategory"]
            category = {
                "CategoryName": CategoryName,
                "Description":Description,
                "ImageCategory":ImageCategory             
            }
            database.child('Category').push(category)
            return HttpResponseRedirect("/Category/")
    else:
        form = AddCategoryForm()
    return render(request, "theme/pages/addcategory.html", {"form": form})

def UpdateCategory(request,id):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            CategoryName = form.cleaned_data["CategoryName"]
            Description = form.cleaned_data["Description"]
            ImageCategory = form.cleaned_data["ImageCategory"]
            category_data = database.child('Category').child(str(id)).get().val()
            category = {
                "CategoryName": CategoryName,
                "Description":Description,
                "ImageCategory":ImageCategory             
            }
            category_data = database.child('Category').child(str(id)).update(category)
            return HttpResponseRedirect("/Category/")
    else:
        form = AddCategoryForm()
        key = database.child('Category').child(str(id)).get()
        data = database.child('Category').child(str(id)).get().val()
    return render(request, "theme/pages/UpdateCategory.html", {"form": form,"data":data,"key":key})    


def EditStatus(request,id,iduser):
    if request.method == "POST":
        form = EditStatusForm(request.POST)
        if form.is_valid():
            Status = form.cleaned_data["Status"]
            value = {
                "Status": Status          
            }
            update_status = database.child('Order').child(str(iduser)).child(str(id)).update(value)
            return HttpResponseRedirect("/order/")
    else:
        form = EditStatusForm()
    return render(request, "theme/pages/EditStatus.html", {"form": form,"id":id,"iduser":iduser})

def CreateOrder(request):
    return render(request, "theme/pages/CreateOrder.html")


    
