from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
     path('add-budget', views.AddBudget.as_view(), name = 'add_budget'),
     path('add-category', views.AddCategory.as_view(), name = 'add_category'),
     path('add-transaction', views.AddTransaction.as_view(), name = 'add_transaction'),
     path('budget-list/', BudgetList.as_view(), name='budget_list'),
     path('category-list/', CategoryList.as_view(), name='category_list'),
     path('transaction-list/', TransactionList.as_view(), name='transaction_list'),

# managebudget

   


      

]