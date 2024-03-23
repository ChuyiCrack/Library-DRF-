from django.db import models
from django.conf import settings
import random

TAGS_BOOKS=['mistery','comedy','history','horror']

class Author(models.Model):
    name=models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.name} {self.id}'
User = settings.AUTH_USER_MODEL  #auth.user

class Book(models.Model):
    user=models.ForeignKey(User,null=True,blank=False, on_delete=models.SET_NULL)
    name=models.CharField(max_length=35)
    description=models.CharField(max_length=150,blank=True)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    existence = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    @property
    def BookShoopPrice(self):
        return self.price*1.2
    @property
    def get_tag(self):
        return random.choice(TAGS_BOOKS)

    def has_ecistence(self):
        return self.existence
    
    def __str__(self):
        return f'{self.name} {self.id}'



