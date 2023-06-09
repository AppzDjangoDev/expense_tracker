from django.shortcuts import redirect, render
from account.forms import UserLoginForm, UserRegisterForm
from django.contrib import auth
from django.views import View  
from django.contrib.auth import logout
from django.contrib import messages
from account.models import User
from django.contrib.auth.decorators import login_required


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


# Registration 
class UserRegisterView(View):

    def get(self, request):
        template = "landing/register.html"
        context={}
        context['form']= UserRegisterForm()
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

    
    def username_generator(self):
        import string
        import random
        # initializing size of string
        N = 7
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        return res
    


    def post(self, request):
        context={}
        form = UserRegisterForm(request.POST)
        context['form']= form
        template = "landing/register.html"
        if request.method == "POST":
            if form.is_valid():
                user_email = request.POST["user_email"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                username = request.POST["username"]
                password1 = request.POST["password1"]
                
                # user creating here 
                user = User.objects.create_user(username=username,
                                            email=user_email,
                                            password=password1,first_name = first_name,last_name = last_name)
                
                print("user_created")
                messages.success(request, 'Registration completed Successfully')
                return render(request, template, context) 
            
            else:
                print("user not created")
                messages.error(request, 'Some Error Occured')
                return render(request, template, context)
            
    def get_username(self):
        username = self.username
        return username
    



class SuccessView(View):
    def get(self, request):
        template = "success_page.html"
        context={}
        print("context", context)
        return render(request, template, context)
        
  

# @login_required(login_url='/login/')
class UserDashBoardView(View):
    def get(self, request):
        template = "user/dashboard.html"
        context={}
        print("context", context)
        return render(request, template, context)
    


class ProfileView(View):
    def get(self, request):
        template = "pages-account-settings-account.html"
        context={}
        print("context", context)
        return render(request, template, context)
    


# class ProfileView(View):

#     def __init__(self):
#         pass

#     def get(self, request):
#         user_pk = request.user
#         try:
#             instance = User.objects.get(pk=user_pk.id)
#         except User.DoesNotExist:
#             instance = None
#         form = UserprofileUpdate(instance=instance)
#         template = "pages-account-settings-account.html"
#         context={}
#         context['form'] = form
#         print("context", context)
#         return render(request, template, context)

#     def post(self, request):
#         user_id = request.user.id
#         instance = get_object_or_404(User, id=user_id)
#         print("11")
#         context={}
#         form = UserprofileUpdate(request.POST or None, request.FILES or None,  instance=instance)
#         context['form']= form
#         template = "pages-account-settings-account.html"

#         if form.is_valid():
#             print("data",request.POST)
#             form.save()
#             print("updated successfully")
#             messages.success(request, 'Your Account details updated successfully!')
#             return redirect('user_dashboard')  
#         else:
#             print("33")
#             print("updating failed")
#             return render(request, template, context)
