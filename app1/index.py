from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Book

@register(Book)  #Its similar like when you need to add the model to admin.py to see it on the django admin panel , here is the same but for the algolias panel
class BookIndex(AlgoliaIndex):
    #should_index='has_ecistence'  #here are like type of conditions if you want to add it or not, here i create a method that if has existance it will show up
    fields=[
        'user',
        'name',
        'description',
        'author',
        'price',
        'existence',
    ]

    settings = {
        'searchableAttributes' : ['name','description'],
        'attributesForFaceting': [ 'user','existence']
    }

    tags='get_tag'