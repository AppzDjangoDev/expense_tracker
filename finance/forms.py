from django import forms
from account.models import User  
from django.core.exceptions import ValidationError
from . models import  *
# from bootstrap_datepicker_plus.widgets import DatePickerInput


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name','start_date', 'end_date', 'total_amount']
        widgets = { 'user': forms.HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['placeholder'] = 'YYYY-mm-dd'
        self.fields['end_date'].widget.attrs['placeholder'] = 'YYYY-mm-dd'
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'

    def form_valid(self, form):
        date_field_value = form.cleaned_data['start_date']
        existing_date_values = Budget.objects.values_list('end_date', flat=True)

        for existing_date in existing_date_values:
            if date_field_value >= existing_date:
                form.add_error('date_field', 'The selected date should be greater than existing dates.')
                return self.form_invalid(form)

        return super().form_valid(form)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description', 'categorytype']
        widgets = { 'user': forms.HiddenInput(), }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'budget', 'amount', 'date']
        widgets = { 'user': forms.HiddenInput(), }
       

    def __init__(self,*args, **kwargs):
        username = kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['category'].queryset = Category.objects.filter(user=username)
            self.fields['budget'].queryset = Budget.objects.filter(user=username)
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'
            


class FinancialgoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = [ 'budget', 'category', 'amount_limit' ]
        widgets = { 'user': forms.HiddenInput(), }
       

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('user')
        super(FinancialgoalForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['category'].queryset = Category.objects.filter(user=username,categorytype='expense')
            self.fields['budget'].queryset = Budget.objects.filter(user=username)
        for visible in self.visible_fields():
            print("visible", visible.field.widget)
            visible.field.widget.attrs['class'] = 'form-control m-2'

