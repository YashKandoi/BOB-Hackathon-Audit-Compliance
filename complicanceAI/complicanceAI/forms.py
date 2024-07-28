from django import forms
from .models import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['name', 'age', 'gender', 'account_type', 'pan_number', 'adhaar_number','bank_statement', 'other_documents']