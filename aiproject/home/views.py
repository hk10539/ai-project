from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def home_page(request):
    name=request.GET.get('name')
    print(name)
    if not name:
        return Response({
            "error":"name parameter required"
        })
    return Response({
        "message":f"Hello {name}"
    })
