from django import forms
from account.models import User  
from django.core.exceptions import ValidationError
from . models import  *
# from bootstrap_datepicker_plus.widgets import DatePickerInput


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name','start_date', 'end_date', 'total_amount']

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'YYYY-mm-dd'
        self.fields['end_date'].widget.attrs['placeholder'] = 'YYYY-mm-dd'
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'budget', 'amount', 'date']
       

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'

