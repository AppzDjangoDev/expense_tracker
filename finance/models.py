from django.db import models
from account.models import User

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    def __str__(self):
       	 return self.name


class Transaction(models.Model):
    CHOICES = (
        ('income', 'INCOME'),
        ('expense', 'EXPENSE'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=CHOICES)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField()
    achieved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)