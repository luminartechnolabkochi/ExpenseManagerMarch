
from django import forms

from myapp.models import Category,Transactions

class CategoryForm(forms.ModelForm):


    class Meta:

        model=Category

        fields=["name","budget","owner"]

        widgets={
            
            "name":forms.TextInput(attrs={"class":"form-control"}),

            "budget":forms.NumberInput(attrs={"class":"form-control"}),

            "owner":forms.TextInput(attrs={"class":"form-control"})

        }





class TransactionForm(forms.ModelForm):

    class Meta:

        model=Transactions

        fields=["title","amount","category_object","payment_method","owner"]

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),

            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),

            "category_object":forms.Select(attrs={"class":"form-control form-select mb-2"}),
            
            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            "owner":forms.TextInput(attrs={"class":"form-control"}),


        }










    




