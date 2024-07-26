from django.http import JsonResponse
from .serializers import GuidelinesSerializer, postGuidelinesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

base_path = './regulations_files/'

@api_view(['GET', 'POST'])
def aml_guidelines(request):
    file = open(base_path+'AML.txt','r', encoding='utf-8')
    contents = file.read()
    if request.method=='GET':
        serializer = GuidelinesSerializer({'file': base_path+'AML.txt', 'content': contents})
        file.close()
        return JsonResponse(serializer.data, safe=False)
    if request.method=='POST':
        serializer = postGuidelinesSerializer(request.data)
        if serializer.is_valid():
            file = open(base_path+'AML.txt','w', encoding='utf-8')
            file.write(serializer.data.content)
            file.close()
            return Response(serializer.data.content, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def kyc_guidelines(request):
    file = open(base_path+'KYC.txt','r', encoding='utf-8')
    contents = file.read()
    if request.method=='GET':
        serializer = GuidelinesSerializer({'file': base_path+'KYC.txt', 'content': contents})
        file.close()
        return JsonResponse(serializer.data, safe=False)
    if request.method=='POST':
        serializer = postGuidelinesSerializer(request.data)
        if serializer.is_valid():
            file = open(base_path+'KYC.txt','w', encoding='utf-8')
            file.write(serializer.data.content)
            file.close()
            return Response(serializer.data.content, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
