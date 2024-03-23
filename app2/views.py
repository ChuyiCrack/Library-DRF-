from django.shortcuts import render
from app1.models import Book
from app1.serializer import BookSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


#if you handle it like this view you need to create 2 urls in the urlpatterns
#But for mor eassier is better handle it with the Classes in the app1
@api_view(['GET','POST'])
def book_alt_view(request,pk=None):
    #2 urls one when you want to retrieve all the objects that would be book/  and the other one for certain object is book/<int:pk>/
    if   request.method   == 'POST':
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'query':'Error'}, status=400)

    elif request.method   == 'GET' :
        if pk is not None:
            obj= get_object_or_404(Book,pk=pk)
            serializer = BookSerializer(obj)
            return Response(serializer.data)
        
        queryset= Book.objects.all()
        serializer = BookSerializer(queryset,many=True)
        return Response(serializer.data)
            
