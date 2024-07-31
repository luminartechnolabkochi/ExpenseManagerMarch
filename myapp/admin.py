from django.contrib import admin

# Register your models here.


from myapp.models import Category,Transactions

admin.site.register(Category)
admin.site.register(Transactions)

# categories = Category.objects.filter(owner="sajay").annotate( total_amount=Sum('transactions__amount'))
#  for category in categories:
        # if category.total_amount is None:
            # category.total_amount = 0