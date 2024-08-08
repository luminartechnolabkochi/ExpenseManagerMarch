
from django.contrib import admin

from django.urls import path

from myapp import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path("category/add/",views.CategoryCreateView.as_view(),name="category-add"),

    path("category/<int:pk>/change/",views.CategoryEditView.as_view(),name="category-edit"),

    path("transaction/add/",views.TransactionCreateView.as_view(),name="transaction-add"),

    path("transactions/<int:pk>/change/",views.TransactionUpdateView.as_view(),name="transaction-change"),
    
    path("transactions/<int:pk>/remove/",views.TransactionDeleteView.as_view(),name="transaction-delete"),

    path("expense/summary/",views.ExpenseSummaryView.as_view(),name="summary"),

    path("transactions/summary/",views.TransactionSummaryView.as_view(),name="transaction-summary"),

    path("chart/",views.ChartView.as_view(),name="chart"),

    path("register/",views.SignUpView.as_view(),name="signup"),

    path("",views.SignInView.as_view(),name="signin"),
    
    path("signout/",views.SignOutView.as_view(),name="signout"),

]

