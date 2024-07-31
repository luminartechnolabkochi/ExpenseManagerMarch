from django.shortcuts import render,redirect

from django.views.generic import View

from django.utils import timezone

from myapp.forms import CategoryForm,TransactionForm

from myapp.models import Category,Transactions

from django.db.models import  Sum



class CategoryCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=CategoryForm()

        qs=Category.objects.all()

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=CategoryForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()          

            return redirect("category-add")
        
        else:

            return render(request,"category_add.html",{"form":form_instance})


# url:lh:8000/category/{int:pk}/change/

class CategoryEditView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        category_object=Category.objects.get(id=id)       

        form_instance=CategoryForm(instance=category_object)

        return render(request,"category_edit.html",{"form":form_instance})
    
 
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        cat_obj=Category.objects.get(id=id)

        form_instance=CategoryForm(request.POST,instance=cat_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("category-add")
        else:
            return render(request,"category_edit.html",{"form":form_instance})




class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionForm()

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year)



        return render(request,"transaction_add.html",{"form":form_instance,"transactions":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,"transaction_add.html",{"form":form_instance})




#url:lh:8000/transactions/{int:pk}/change/

class TransactionUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transactions.objects.get(id=id)

        form_instance=TransactionForm(instance=trans_obj)

        return render(request,"transaction_edit.html",{"form":form_instance})


    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        trans_obj=Transactions.objects.get(id=id)

        form_instance=TransactionForm(request.POST,instance=trans_obj)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("transaction-add")
        
        else:

            return render(request,"transaction_edit.html",{"form":form_instance})



class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect("transaction-add")


from django.db.models import Sum
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        qs=Transactions.objects.filter(
                                            created_date__month=cur_month,
                                            created_date__year=cur_year
                                    )
        
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))
        
        print(total_expense)

        return render(request,"expense_summary.html")


            



    





