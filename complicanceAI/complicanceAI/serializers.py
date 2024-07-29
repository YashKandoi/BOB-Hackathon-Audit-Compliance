from rest_framework import serializers
from .models import BankAccount

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

class GuidelinesSerializer(serializers.Serializer):
    file = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=1000)
    class Meta:
        fields = ['file', 'content']

class postGuidelinesSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
    class Meta:
        fields = ['content']

class BankAccountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)
    pan_number = serializers.CharField(max_length=10)
    adhaar_number = serializers.CharField(max_length=12)
    bank_statement = serializers.FileField(required=False)
    other_documents = serializers.FileField(required=False)
    insights = serializers.CharField(required=False)

    class Meta:
        model = BankAccount
        fields = ["name", "age", "gender", "account_type", "pan_number", "adhaar_number", "bank_statement", "other_documents", "insights"]
        some_optional_fields = ["bank_statement", "other_documents", "insights"]
        extra_kwargs = {}
        for field in some_optional_fields:
           extra_kwargs[field] = {'required': False, 'allow_blank': True}