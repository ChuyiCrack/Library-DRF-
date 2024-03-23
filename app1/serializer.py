from rest_framework import serializers
from .models import Book
from . import validators

# class BookInlineSerializer(serializers.Serializer):
#     name = serializers.CharField(read_only=True)
#     url = serializers.HyperlinkedIdentityField(
#         view_name='book_detail',
#         lookup_field = 'pk',
#         read_only=True
#     )

class UserPublicSErializer(serializers.Serializer):
    username= serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # other_books=serializers.SerializerMethodField(read_only=True)


    # def get_other_books(self,obj):
    #     request=self.context.get('request')                                         #All this code in green show Other books that the user Has, it show it randomly
    #     user = obj
    #     my_books=  user.book_set.all().order_by('?')[:2]
    #     return BookInlineSerializer(my_books, many=True,context={'request': request}).data

class AuthorPublicSErializer(serializers.Serializer):
    name= serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)



class BookSerializer(serializers.ModelSerializer):
    tag= serializers.SerializerMethodField(read_only=True)
    Shop_Price=serializers.SerializerMethodField(read_only=True)
    #user=serializers.SerializerMethodField(read_only=True)
    owner= UserPublicSErializer(source='user',read_only=True)
    #author= AuthorPublicSErializer(read_only=True)
    email= serializers.EmailField(write_only=True,required=False)  #thi email field is write only, is not in the Book Model but when you are saving the object you need to remove at the moment to save cause it will cause an error but thi can help you for only retrieving data
    # << edit_url=serializers.SerializerMethodField(read_only=True) >>
    url = serializers.HyperlinkedIdentityField(
        view_name='book_detail',
        lookup_field='pk'
    )

    name= serializers.CharField(validators=[validators.no_bad_words,validators.unique_book_name]) #It will check this custom validator in validators.py  and if it fullfill the condition for the name will create the object
    class Meta:
        model=Book
        fields=['url','email','owner','tag','pk','name','author', 'description', 'price', 'Shop_Price']
                      #  ^  we add email but it will no be show in the json its only for creating new books it will be required
    #Are 2 forms of adding links to the serializer but for me is more easier the second option, all the first option is commente and symbolized
    
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # def get_edit_url(self,obj):
    #     request = self.context.get('request')  #is like the self.request, but we need to add it like this because sometimes it doesnt appear and we will verify it wit an if

    #     if request is None:
    #         return None
        
    #     return reverse('Book-Edit', kwargs={'pk':obj.pk}, request=request)
                   #  Url path name       pk of the object        
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    def get_tag(self,obj):
        return obj.get_tag
    
    def get_Shop_Price(self,obj):
        return obj.BookShoopPrice
    
    # def get_user(self,obj):
    #     return obj.user.username
    
class BookSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['name', 'description', 'price']

    #This one will update if it see a new change
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name', instance.name)
        instance.description=validated_data.get('description', instance.description)
        instance.price=validated_data.get('price', instance.price)
        instance.save()
        return instance
    

class BookSerializerSearch(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= ['name','description','author','price']