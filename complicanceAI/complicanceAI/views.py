from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

base_path = '../azure/RBI_Guidelines_Documents/j_rbi_data_1.txt'

def rbi_guidelines(request):
    file = open(base_path,'r')
    contents = file.read()
    return HttpResponse(contents)
