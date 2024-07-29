from django.db import models

GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

ACCOUNT_TYPE_CHOICES = [
        ('SAVINGS', 'Savings'),
        ('CURRENT', 'Current'),
        ('SALARY', 'Salary'),
        ('FD', 'Fixed Deposit'),
        ('RD', 'Recurring Deposit'),
        ('NRI', 'NRI'),
    ]

class Compliances(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class BankAccount(models.Model):
    name = models.CharField(max_length=255, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, null=False)
    pan_number = models.CharField(max_length=10, unique=True, null=False)
    adhaar_number = models.CharField(max_length=12, unique=True, null=False)
    bank_statement = models.FileField(upload_to=f'{name}_{account_type}_bankStatement/', blank=True, null=True)
    other_documents = models.FileField(upload_to=f'{name}_{account_type}_documents/', blank=True, null=True) # like Bank Statement, Salary Slip, etc.
    insights = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.name} - {self.account_type}"