from django import forms
import pyrebase

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

class NameForm(forms.Form):
    ImageProduct = forms.URLField(label="Image URL")
    Category = forms.ChoiceField(label="Category",choices=[])
    Price = forms.DecimalField(label="Price")
    Description = forms.CharField(label="Description", widget=forms.Textarea)
    ProductName = forms.CharField(label="Product Name", max_length=100)
    ImageDetail1 = forms.URLField(label="Image URL1")
    ImageDetail2 = forms.URLField(label="Image URL2")
    ImageDetail3 = forms.URLField(label="Image URL3")
    ImageDetail4 = forms.URLField(label="Image URL4")
    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        array = database.child('Category').get()
        category_choices = [(item.val()["CategoryName"], item.val()["CategoryName"]) for item in array.each()]
        self.fields['Category'] = forms.ChoiceField(label="Category", choices=category_choices, required=True)

class UpdateProduct(forms.Form):
    # ID = forms.CharField(label="ID")
    ImageProduct = forms.URLField(label="Image URL")
    Price = forms.DecimalField(label="Price")
    Description = forms.CharField(label="Description", widget=forms.Textarea)
    ProductName = forms.CharField(label="Product Name", max_length=100)
    ImageDetail1= forms.URLField(label="Image URL1")
    ImageDetail2 = forms.URLField(label="Image URL2")
    ImageDetail3 = forms.URLField(label="Image URL3")
    ImageDetail4 = forms.URLField(label="Image URL4")

class UpdateUser(forms.Form):
    ID = forms.CharField(label="ID")
    FirstName = forms.CharField(label="First Name" , max_length=100)
    LastName = forms.CharField(label="Last Name" , max_length=100)
    Password = forms.CharField(label="Password", max_length=100)
    PhoneNumber = forms.DecimalField(label="Phone Number")

class UserForm(forms.Form):
    FirstName = forms.CharField(label="First Name" , max_length=100)
    LastName = forms.CharField(label="Last Name" , max_length=100)
    Password = forms.CharField(label="Password", max_length=100)
    PhoneNumber = forms.DecimalField(label="Phone Number")

class AddCategoryForm(forms.Form):
    CategoryName = forms.CharField(label="Category")
    Description = forms.CharField(label="Description", widget=forms.Textarea)
    ImageCategory = forms.URLField(label="ImageCategory")

class EditStatusForm(forms.Form):
    Status = forms.ChoiceField(label="Status",choices=[])
    def __init__(self, *args, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)
        array = database.child('Status').get()
        status_choices = [(item.val()["Status"], item.val()["Status"]) for item in array.each()]
        self.fields['Status'] = forms.ChoiceField(label="Status", choices=status_choices, required=True)


    