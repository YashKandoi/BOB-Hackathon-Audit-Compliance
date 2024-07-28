from django.http import JsonResponse
from .serializers import GuidelinesSerializer, postGuidelinesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .forms import BankAccountForm
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
def create_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace 'success_url' with your desired URL
    else:
        form = BankAccountForm()
    return render(request, 'create_bank_account.html', {'form': form})