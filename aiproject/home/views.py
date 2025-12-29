from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from PyPDF2 import PdfReader, PdfMerger, PdfWriter

# Create your views here.
@api_view(['POST'])
def pdf_length(request):
    pdf_file=request.FILES.get('pdf')
    reader=PdfReader(pdf_file)
    if pdf_file and pdf_file.name.endswith('pdf'):
        return Response(
            {"message": len(reader.pages)},
            status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"message": "Not get"},
            status=status.HTTP_400_BAD_REQUEST
            )


# Create your views here.
@api_view(['POST'])
def metadata(request):
    pdf_file=request.FILES.get('pdf')
    reader=PdfReader(pdf_file)
    if pdf_file and pdf_file.name.endswith('pdf'):
        return Response(
            {"message": reader.metadata},
            status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"message": "Not get"},
            status=status.HTTP_400_BAD_REQUEST
            )
    
# Create your views here.
@api_view(['POST'])
def readdata(request):
    pdf_file=request.FILES.get('pdf')
    reader=PdfReader(pdf_file)
    if pdf_file and pdf_file.name.endswith('pdf'):
        return Response(
            {"message": reader.pages[0].extract_text()},
            status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"message": "Not get"},
            status=status.HTTP_400_BAD_REQUEST
            )