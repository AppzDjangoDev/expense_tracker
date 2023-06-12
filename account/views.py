from django.shortcuts import redirect, render
from account.forms import UserLoginForm, UserprofileUpdate
from django.contrib import auth
from django.views import View  
from django.contrib.auth import logout
from django.contrib import messages
from account.models import User
from finance.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class UserloginView(View):
    def get(self, request):
        template = "landing/login.html"
        context={}
        context['form']= UserLoginForm()
        print("context", context)
        logged_user = request.user

        if logged_user.is_authenticated:
            print(logged_user)
            print("dashboard__form")
            return redirect('user_dashboard')  
        else:
            print(logged_user)
            print("login__form")
            return render(request, template, context)
        
    def logoutUser(request):
        print("logout_processing")
        logout(request)
        return redirect('login')

    def post(self, request):
        context={}
        form = UserLoginForm(request.POST)
        context['form']= form
        template = "landing/login.html"
        if request.method == "POST":
            if form.is_valid():
                login_username = request.POST["username"]
                login_password = request.POST["password"]
                print(login_username)
                print(login_password)
                user = auth.authenticate(username=login_username, password=login_password)
                if user :
                # if user is not None and  user.is_superuser==False and user.is_active==True:
                    auth.login(request, user)
                    print("login success")
                    messages.success(request, "Login Successful !")
                    # return render(request, "user/dashboard.html")
                    return redirect('user_dashboard')  
                else:
                    print("user not Exists")
                    # messages.info(request, "user not Exists")
                    messages.error(request, 'Username or Password incorrect !')
                    return render(request, template, context)
            else:
                print("user not created")
                return render(request, template, context)

def homePage(request):
    return render(request,'landing/landing_page.html')



class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "landing/register.html"
    success_url = reverse_lazy('user_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Authenticate and log in the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        messages.success(self.request, 'Registration completed successfully')
        user = authenticate(username=username, password=password)
        messages.success(self.request, 'redirected to Dashboard')
        login(self.request, user)
        return response

class MemberListView(View):
    def get(self, request , **kwargs):
        template = "user/accountmanage.html"
        breadcrumb = {"1":"Member Management", "2":"Manage member" }
        label = { 'title' : "Manage member" }
        header = { "one": 'First Name',"two" : 'Last Name', "three" : "User Name",}
        Data =  User.objects.all()
        context = {'header':header , 'label':label, "breadcrumb":breadcrumb ,"Data": Data}
        return render(request, template, context)

class SuccessView(View):
    def get(self, request):
        template = "success_page.html"
        context={}
        print("context", context)
        return render(request, template, context)
        
# @login_required(login_url='/login/')
class UserDashBoardView(LoginRequiredMixin,View):
    def get(self, request):
        template = "user/dashboard.html"
        context={}
        print("self.request__dashboard", self.request.user.id)

        current_datetime = datetime.now()
        # get budget details
        try:
            current_budget = Budget.objects.filter(end_date__gte=current_datetime, user = self.request.user.id).get()
            if current_budget:
                modalcontent = {'title': 'Not Allowed to  add budget for Now', 'description': 'You can only add Budget After the Current budget End Date'}
                context['modalcontent'] = modalcontent
                context['current_budget'] = current_budget
                budget = current_budget
                
        except:
            try:
                previous_budget = Budget.objects.filter(end_date__gte=current_datetime, user = self.request.user.id).get()
                context['previous_budget'] = previous_budget
                budget = current_budget
            except Budget.DoesNotExist:
                pass
        try :
            get_income_data = Transaction.objects.filter(category__categorytype ='income',budget=budget,user = self.request.user.id).aggregate(total_amount=Sum('amount'))
            if get_income_data:
                # income_total = get_income_data['total_amount']
                get_income_data['total_amount'] = get_income_data['total_amount'].quantize(Decimal('0.00'))
                context['get_income_data'] = get_income_data
        except:
            get_income_data = {}
            get_income_data['total_amount'] = Decimal(0).quantize(Decimal('0.00'))
        try :
            get_expense_data = Transaction.objects.filter(category__categorytype ='expense',budget=budget, user = self.request.user.id).aggregate(total_amount=Sum('amount'))
            if get_expense_data:
                get_expense_data['total_amount'] = get_expense_data['total_amount'].quantize(Decimal('0.00'))
                context['get_expense_data'] = get_expense_data

        except:
            get_expense_data = {}
            get_expense_data['total_amount'] = Decimal(0).quantize(Decimal('0.00'))

            

        if get_income_data and get_expense_data:
            print("get__data")
            balance_amount = get_income_data['total_amount'] - get_expense_data['total_amount']
            print("______________________________")
            print(get_income_data['total_amount'])
            print(get_expense_data['total_amount'], "1111111", type(balance_amount))
            balance_amount_decimal = balance_amount.quantize(Decimal('0.00'))
            print("______________________________", balance_amount_decimal)
            context['balance_amount_decimal'] = balance_amount_decimal

        try:
            # get table data 
            income_transactions =  Transaction.objects.filter(category__categorytype='income',  user = self.request.user.id, budget=budget)
            if income_transactions:
                context['income_transactions'] = income_transactions


            expense_transactions =  Transaction.objects.filter(category__categorytype='expense',  user = self.request.user.id, budget=budget)
            if expense_transactions:
                context['expense_transactions'] = expense_transactions




        # ------------------------------------------------------------------
        # goal data and progress
            from django.db.models import ExpressionWrapper, F
            finance_goals = FinancialGoal.objects.filter(user=self.request.user.id, budget=budget).annotate(percentage=ExpressionWrapper((F('achieved_amount') * 100) / F('amount_limit'), output_field=models.FloatField()))

            # finance_goals = FinancialGoal.objects.filter(user = self.request.user.id, budget = budget).aggregate(ratio_value=ExpressionWrapper(F('achieved_amount') / F('amount_limit'), output_field=models.FloatField()))['ratio_value']
            print("finance_goals", type(finance_goals))
            if finance_goals:
                context['finance_goals'] = finance_goals


        # progress_dict = {}
        
        # for expdata in expense_transactions:
        #     print(expdata.category, )
        #     for gdata in goaldata:
        #         if expdata.category == gdata.category:
        #             progress_dict['expense'] : [expdata.category, expdata.amount]

        except: 
            pass



        

        

        





                
        





        





        
        

        
        
        print("context", context)
        return render(request, template, context)

class ProfileView(View):
    def __init__(self):
        pass

    def get(self, request):
        user_pk = request.user
        try:
            instance = User.objects.get(pk=user_pk.id)
        except User.DoesNotExist:
            instance = None
        form = UserprofileUpdate(instance=instance)
        template = "pages-account-settings-account.html"
        context={}
        context['form'] = form
        print("context", context)
        return render(request, template, context)

    def post(self, request):
        user_id = request.user.id
        instance = get_object_or_404(User, id=user_id)
        context={}
        form = UserprofileUpdate(request.POST or None, request.FILES or None,  instance=instance)
        context['form']= form
        template = "pages-account-settings-account.html"
        if form.is_valid():
            form.save()
            print("updated successfully")
            messages.success(request, 'Your Account details updated successfully!')
            return redirect('user_dashboard')  
        else:
            print("updating failed")
            return render(request, template, context)