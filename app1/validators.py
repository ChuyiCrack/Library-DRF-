from rest_framework import serializers
from .models import Book
from rest_framework.validators import UniqueValidator



def no_bad_words(value):
    bad_words=['pene','vagina','sexo','cancer','negros','nazzi','nigger']
    for bad_word in bad_words:
        if bad_word in value.lower():
            raise serializers.ValidationError(f'You can not use bad words')
    
    return value

unique_book_name= UniqueValidator(queryset=Book.objects.all(),lookup='iexact')   #This checks if there is any book that has the same name if Yes it wont create the object an will say thats needs to be unique



