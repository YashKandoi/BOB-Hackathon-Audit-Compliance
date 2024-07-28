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
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    pan_number = models.CharField(max_length=10, unique=True)
    adhaar_number = models.CharField(max_length=12, unique=True)
    other_documents = models.FileField(upload_to=f'{name}_{account_type}_documents/', blank=True, null=True) # like Bank Statement, Salary Slip, etc.

    def __str__(self):
        return f"{self.name} - {self.account_type}"