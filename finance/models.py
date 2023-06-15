from django.db import models
from account.models import User
from datetime import date


class Budget(models.Model):
    name =  models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today().strftime('%Y-%m-%d'))
    end_date = models.DateField(default=date.today().strftime('%Y-%m-%d'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
       	 return self.name


class Category(models.Model):
    CHOICES = (
        ('income', 'INCOME'),
        ('expense', 'EXPENSE'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    categorytype = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
       	 return self.name
    



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today().strftime('%Y-%m-%d'))



class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    achieved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)



class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)