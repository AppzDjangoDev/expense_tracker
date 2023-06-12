from django.shortcuts import render
from . models import *
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from . forms import BudgetForm, TransactionForm, CategoryForm
from django.views import View  
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv



class AddBudget(CreateView):
    form_class =  BudgetForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'

    def form_valid(self, form):
        form.instance.user = self.request.user 
        response = super().form_valid(form)
        form_class = self.get_form_class()  # Get the form class
        form = form_class()  # Create a new instance of the form
        self.object = None  # Clear the object reference
        return response

    def get_context_data(self, **kwargs):
        ctx = super(AddBudget, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Budget"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx



class AddCategory(CreateView):
    form_class =  CategoryForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'

    def form_valid(self, form):
        response = super().form_valid(form)
        form_class = self.get_form_class()  # Get the form class
        form = form_class()  # Create a new instance of the form
        self.object = None  # Clear the object reference
        return response

    def get_context_data(self, **kwargs):
        ctx = super(AddCategory, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Category"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx



class AddTransaction(CreateView):
    form_class =  TransactionForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'
  

    def form_valid(self, form):
        form.instance.user = self.request.user 
        response = super().form_valid(form)
        form_class = self.get_form_class()  # Get the form class
        form = form_class()  # Create a new instance of the form
        self.object = None  # Clear the object reference
        return response

    def get_context_data(self, **kwargs):
        ctx = super(AddTransaction, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Category"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx


from django.views.generic.list import ListView

 
class BudgetList(ListView):
    # specify the model for list view
    model = Budget
    template_name = "finance/listview.html"

    def get_context_data(self, **kwargs):
        ctx = super(BudgetList, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Budget List"
        }
        headerlist = ['Budget Name', 'Start Date', 'End Date', 'Username','Limit Amount', 'download CSV']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
        ctx['actions'] = True


        return ctx


class CategoryList(ListView):
    # specify the model for list view
    model = Category
    template_name = "finance/listview.html"

    def get_context_data(self, **kwargs):
        ctx = super(CategoryList, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Category List"
        }
        headerlist = ['Category Name', 'description', 'categorytype']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
        return ctx


class TransactionList(ListView):
    # specify the model for list view
    model = Transaction
    template_name = "finance/listview.html"

    def get_context_data(self, **kwargs):
        ctx = super(TransactionList, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Transaction List"
        }
        headerlist = [ 'Category', 'Budget', 'Amount','Username', 'Date']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
        return ctx


def export_financial_data(request,**kwargs):
    print("kwargs", kwargs)
    budget_id = kwargs['slug']
    transcation_mode = kwargs['trans_mode']
    print("budget_id", budget_id)

    getBudget = Budget.objects.filter(id=budget_id ).get()

    print("getBudget", getBudget) 

    template = "user/dashboard.html"
    context={}
    # Retrieve the financial data from your models or other data sources
    financial_data = Transaction.objects.filter(category__categorytype = transcation_mode, budget=getBudget )

    print("financial_data", financial_data)

    # Create the HttpResponse object with CSV mime type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    print('writer', writer)
    transaction_mode = transcation_mode.upper()
    print('transaction_mode', transaction_mode)

    # Write the header row
    writer.writerow(['Transaction date', 'Category', 'Amount','Budget', 'transaction_mode' ])  # Replace with your column names

    # Write the data rows
    for data in financial_data:
        writer.writerow([data.date, data.category, data.amount, data.budget, transaction_mode ])  # Replace with your field names

    return response
