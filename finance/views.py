from django.shortcuts import render
from . models import *
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from . forms import BudgetForm, TransactionForm, CategoryForm, FinancialgoalForm
from django.views import View  
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import F


class AddBudget(CreateView):
    form_class =  BudgetForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'

    def form_valid(self, form):
        print("pppppp")
        if form.is_valid():
            print("pppp----")
            budget = form.save(commit=False)
            print("self.request.user.id", self.request.user.id)
            budget.user = User.objects.get(id=self.request.user.id) 
            budget.save()
            response = super().form_valid(form)
            return response
        
        else:
            print("pppp----pp")
            return JsonResponse({'message': 'Invalid form data.'}, status=400)

    def get_context_data(self, **kwargs):
        ctx = super(AddBudget, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Budget"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx
    
    def dispatch(self, request, *args, **kwargs):
        # Add your custom logic here
        current_date = date.today()
        exist_data_check = Budget.objects.filter(user= request.user, end_date__gte=current_date).exists()
        print("exist_data_check", exist_data_check)
        if exist_data_check: 
            messages.warning(request, 'Your can add budget only after the Current Budget End date')
            return redirect('user_dashboard')  
        return super().dispatch(request, *args, **kwargs)
    



class AddCategory(CreateView):
    form_class =  CategoryForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'
    
    def form_valid(self, form):
        print("self.request.user.id", self.request.user.id)
        category = form.save(commit=False)
        exist_data_check = Category.objects.filter(user=self.request.user.id, name = category.name).exists()
        if exist_data_check:
            messages.warning(self.request, 'Duplicate Category name')
            return redirect('user_dashboard') 

        print("self.request.user.id", self.request.user.id)
        category.user = User.objects.get(id=self.request.user.id) 
        category.save()
        messages.success(self.request, 'saved successfully')
        response = super().form_valid(form)
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
        transaction = form.save(commit=False)
        print("self.request.user.id", self.request.user.id)
        transaction.user = User.objects.get(id=self.request.user.id) 
        transaction.save()
        messages.success(self.request, 'saved successfully')
        response = super().form_valid(form)
        print("transaction__test", transaction.category)
        # updating_to goal progress amount
        try :
            goal_check = FinancialGoal.objects.filter(category=transaction.category,budget=transaction.budget,user=self.request.user.id).get()
            if goal_check.category:
                print('goal_check_category', goal_check.category)
                check_type = Category.objects.filter(name = goal_check.category,categorytype='expense').exists()
                if check_type:
                    print("check_type_____________--", check_type)
                    FinancialGoal.objects.filter(category=transaction.category,budget=transaction.budget,user=self.request.user.id).update(achieved_amount=F('achieved_amount') + transaction.amount)
            print("goal_check", goal_check.__dict__)
    
        except:
            pass
            

        
        
        return response

    def get_context_data(self, **kwargs):
        ctx = super(AddTransaction, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Transaction"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx

class AddFinancialgoal(CreateView):
    form_class =  FinancialgoalForm
    template_name = "finance/addtemplate.html"
    success_url = '/dashboard'

    def form_valid(self, form):
        financialgoal = form.save(commit=False)
        print("self.request.user.id", self.request.user.id)
        financialgoal.user = User.objects.get(id=self.request.user.id) 
        existingcheck = FinancialGoal.objects.filter(budget=financialgoal.budget,category=financialgoal.category ).exists()
        if existingcheck:
            messages.warning(self.request, 'Duplicate Entry for the Same Budget')
            return redirect('user_dashboard')  
        else:
            financialgoal.save()
            messages.success(self.request, 'Saved successfully')
            response = super().form_valid(form)
            return response

    def get_context_data(self, **kwargs):
        ctx = super(AddFinancialgoal, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Add Financialgoal"
        }
        ctx['breadcrumb'] = breadcrumb
        return ctx


from django.views.generic.list import ListView
class BudgetList(LoginRequiredMixin ,ListView):
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

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(user=user)
        return filtered_queryset
    



class CategoryList(LoginRequiredMixin ,ListView):
    # specify the model for list view
    model = Category
    template_name = "finance/listview.html"

    def get_context_data(self, **kwargs):
        ctx = super(CategoryList, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"Category List"
        }
        headerlist = ['Category Name', 'description','username','category type']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
        return ctx

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(user=user)
        return filtered_queryset


class TransactionList(LoginRequiredMixin ,ListView):
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

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(user=user)
        return filtered_queryset



class FinancialGoalList(LoginRequiredMixin ,ListView):
    # specify the model for list view
    model = FinancialGoal
    template_name = "finance/listview.html"

    def get_context_data(self, **kwargs):
        ctx = super(FinancialGoalList, self).get_context_data(**kwargs)
        breadcrumb = {
            "1":"Finanace Management",
            "2":"FinancialGoal List"
        }
        headerlist = [ 'Category', 'Budget', 'Amount','Username', 'Date']
        ctx['breadcrumb'] = breadcrumb
        ctx['headerlist'] = headerlist
        return ctx

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(user=user)
        return filtered_queryset



def export_financial_data(request,**kwargs):
    print("kwargs", kwargs)
    budget_id = kwargs['slug']
    transaction_mode = kwargs['trans_mode']
    print("budget_id", budget_id)

    getBudget = Budget.objects.filter(id=budget_id ).get()

    print("getBudget", getBudget) 

    template = "user/dashboard.html"
    context={}
    # Retrieve the financial data from your models or other data sources
    financial_data = Transaction.objects.filter(category__categorytype = transaction_mode, budget=getBudget )

    print("financial_data", financial_data)

    # Create the HttpResponse object with CSV mime type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    print('writer', writer)
    transaction_mode = transaction_mode.upper()
    print('transaction_mode', transaction_mode)

    # Write the header row
    writer.writerow(['Transaction date', 'Category', 'Amount','Budget', 'transaction_mode' ])  # Replace with your column names

    # Write the data rows
    for data in financial_data:
        writer.writerow([data.date, data.category, data.amount, data.budget, transaction_mode ])  # Replace with your field names

    return response
