
from typing import Any
from django import forms

from myapp.models import Category,Transactions



class CategoryForm(forms.ModelForm):


    def __init__(self,*args,**kwargs):

        self.user=kwargs.pop("user")

        return super().__init__(*args,**kwargs)


   

    class Meta:

        model=Category

        fields=["name","budget"]

        widgets={
            
            "name":forms.TextInput(attrs={"class":"form-control"}),

            "budget":forms.NumberInput(attrs={"class":"form-control"}),

           

        }

    def clean(self):

        self.cleaned_data=super().clean()#{"name":,"budget":45}

        budget_amount=int(self.cleaned_data.get("budget"))

        print(self.user,"inside cat form")

        if budget_amount<150:

            self.add_error("budget","amount > 150")

        category_name=self.cleaned_data.get("name")

        owner=self.user

        is_exist=Category.objects.filter(name__iexact=category_name,owner=owner).exists()

        if is_exist:

            self.add_error("name","category with this name already exist")

        
        

        return self.cleaned_data
 
    


    





class TransactionForm(forms.ModelForm):

    class Meta:

        model=Transactions

        fields=["title","amount","category_object","payment_method"]

        widgets={

            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),

            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),

            "category_object":forms.Select(attrs={"class":"form-control form-select mb-2"}),
            
            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-2"}),

            


        }


    
class TransactionFilterForm(forms.Form):

    start_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))

    end_date=forms.DateField(widget=forms.DateInput(attrs={"class":"form-control","type":"date"}))
    

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2"]



class LoginForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField()

    



