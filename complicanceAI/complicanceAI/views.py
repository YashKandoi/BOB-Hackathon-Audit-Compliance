from django.http import JsonResponse
from .serializers import GuidelinesSerializer, postGuidelinesSerializer, BankAccountSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from complicanceAI.models import BankAccount
import os

base_path = './regulations_files/'

@api_view(['GET', 'POST'])
def aml_guidelines(request):
    file_path = os.path.join(base_path, 'AML.txt')

    if request.method == 'GET':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
            serializer = GuidelinesSerializer({'file': file_path, 'content': contents})
            return JsonResponse(serializer.data, safe=False)
        except FileNotFoundError:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        serializer = postGuidelinesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(serializer.validated_data['content'])
                return Response(serializer.validated_data['content'], status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def kyc_guidelines(request):
    file_path = os.path.join(base_path, 'KYC.txt')

    if request.method == 'GET':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
            serializer = GuidelinesSerializer({'file': file_path, 'content': contents})
            return JsonResponse(serializer.data, safe=False)
        except FileNotFoundError:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = postGuidelinesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(serializer.validated_data['content'])
                return Response(serializer.validated_data['content'], status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def bank_accounts(request):
    if request.method == 'GET':
        bank_accounts = BankAccount.objects.all()
        serializer = BankAccountSerializer(bank_accounts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

