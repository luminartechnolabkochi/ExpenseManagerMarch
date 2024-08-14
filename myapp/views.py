from django.shortcuts import render,redirect

from django.views.generic import View

from django.utils import timezone

from myapp.forms import CategoryForm,TransactionForm,TransactionFilterForm,RegistrationForm,LoginForm

from myapp.models import Category,Transactions

from django.db.models import  Sum

from django.contrib.auth import authenticate,login,logout

from django.db.models import Sum, F,Q

from django.contrib import messages

from myapp.decorators import signin_required

from django.utils.decorators import method_decorator

# function_dec => method_deco dispatch

# @method_decoartor(signin_requird,name="dispatch")

@method_decorator(signin_required,name="dispatch")
class CategoryCreateView(View):

    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        

        form_instance=CategoryForm(user=request.user)

        qs=Category.objects.filter(owner=request.user)

        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")



        form_instance=CategoryForm(request.POST,user=request.user,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user           

            form_instance.save()                      

            return redirect("category-add")
        
        else:

            return render(request,"category_add.html",{"form":form_instance})


# url:lh:8000/category/{int:pk}/change/

@method_decorator(signin_required,name="dispatch")
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



@method_decorator(signin_required,name="dispatch")
class TransactionCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionForm()

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        categories=Category.objects.filter(owner=request.user)

        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)



        return render(request,"transaction_add.html",{"form":form_instance,"transactions":qs,"categories":categories})
    
    def post(self,request,*args,**kwargs):

        form_instance=TransactionForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("transaction-add")
        else:
            return render(request,"transaction_add.html",{"form":form_instance})




#url:lh:8000/transactions/{int:pk}/change/
@method_decorator(signin_required,name="dispatch")
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


@method_decorator(signin_required,name="dispatch")
class TransactionDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Transactions.objects.get(id=id).delete()

        return redirect("transaction-add")


from django.db.models import Sum
@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        qs=Transactions.objects.filter(
                                            created_date__month=cur_month,
                                            created_date__year=cur_year
                                    )
        
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))

        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))
        
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))

        print(payment_summary)


        data={
            "total_expense":total_expense.get("total"),
            "category_summary":category_summary,
            "payment_summary":payment_summary

        }

        # //testing

        print("test")

        categories = Category.objects.filter(owner=request.user).annotate(
                                                            total_spent=Sum(
                                                                'transactions__amount'
                                                                ,
                                                                  filter=Q(transactions__owner=request.user)
                                                                  )
                                                                ).annotate(
                                                                balance_amount=F('budget') - F('total_spent')
                                                                )
        
        print(categories)

        
        for category in categories:

            if category.total_spent is None:

                category.total_spent = 0

            if category.balance_amount is None:

                category.balance_amount = category.budget

        print( [[c,c.total_spent,c.balance_amount]for c in categories])

        

        return render(request,"expense_summary.html",data)


            



@method_decorator(signin_required,name="dispatch") 
class TransactionSummaryView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TransactionFilterForm()

        cur_month=timezone.now().month

        cur_year=timezone.now().year


        if "start_date" in request.GET and "end_date" in request.GET:

            st_date=request.GET.get("start_date")

            end_date=request.GET.get("end_date")

            qs=Transactions.objects.filter(
                                                created_date__range=(st_date,end_date)

                                            )

                                            # total

        else:    
            
            qs=Transactions.objects.filter(
                                            created_date__month=cur_month,
                                            created_date__year=cur_year
                                            )
        return render(request,"transaction_summary.html",{"transactions":qs,"form":form_instance})



class ChartView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"chart.html")
    
    

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # data=form_instance.cleaned_data
            # User.objects.create(**data)

            form_instance.save()

            messages.success(request,"account created successfully")
            

            print("account created successfully")

            return redirect("signin")
        else:
            print("failed to create account")

            messages.error(request,"failed to create account")

            return render(request,"register.html",{"form":form_instance})


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instnce=LoginForm()

        return render(request,"login.html",{"form":form_instnce})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_obj=authenticate(request,**data)

            if user_obj:

                login(request,user_obj)

                messages.success(request,"login successfully")

                return redirect("summary")
            
        messages.error(request,"failed to login")
        
        return render(request,"login.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
