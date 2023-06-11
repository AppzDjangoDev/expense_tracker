from django.shortcuts import render
from . models import *
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from . forms import BudgetForm, TransactionForm, CategoryForm


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
        headerlist = ['Budget Name', 'Start Date', 'End Date', 'Username','Limit Amount']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
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