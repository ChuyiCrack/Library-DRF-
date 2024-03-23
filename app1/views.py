from django.shortcuts import render
from .models import Book
from .serializer import BookSerializer, BookSerializerUpdate,BookSerializerSearch
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from django.views import View
from rest_framework.generics import RetrieveAPIView,CreateAPIView, UpdateAPIView, DestroyAPIView,GenericAPIView,ListAPIView
from rest_framework import mixins
from .mixins import SraffEditorPermissionMixin, UserQuerySetMixin
from django.db.models import Q
from . import client


class Index(View):
    template_name= 'index.html'
    context={

    }
    def get(self,request):
        return render(request,self.template_name,self.context)


@api_view(['GET','POST'])
def Books(request):
    if request.method == 'GET':
        all_books=Book.objects.all().order_by('?').first()
        serializer = BookSerializer(all_books,context={'request': request})
        return JsonResponse(serializer.data, )
    
    if request.method == 'POST':
        serializer = BookSerializer(data = request.data,context={'request': request})
        if serializer.is_valid():
            email = serializer.validated_data.pop('email')
            print(email)
            serializer.save()
            return JsonResponse(serializer.data)
        print('no valid')
        return JsonResponse({'error':str(serializer.ValidationError)})
    

# class BookViewset(ModelViewSet):
#     queryset=Book.objects.all()
#     serializer_class=BookSerializer
#     filter_backends= [DjangoFilterBackend,SearchFilter,OrderingFilter]
#     filterset_class =BookFilter
#     search_fields = ['name','description']
#     ordering_fields = ['price']

#The REtrieveAPIView works when you want to retrieve a ceratin object, so depending of the url it will show x object.
class BookDetailAPIView(RetrieveAPIView):
    queryset= Book.objects.all()
    serializer_class = BookSerializer

#Is like the same as above but this one is especially to create new instances
class BookCreateAPIView(CreateAPIView):
    queryset= Book.objects.all()
    serializer_class = BookSerializer
    # authentication_classes = [authentication.SessionAuthentication]   << How we add it to the DEfault permission in settings.py we can remove it and it will still working >>
    # permission_classes= [permissions.IsAuthenticated] 

    #this function will be called when it wants to create a new instance,
    # IMPORTANT if you add this function you need to save the serializer to add it to the DB.
    def perform_create(self, serializer):
        #here we will want to add a default description if the user does not add any description.

        name= serializer.validated_data.get('name')
        description= serializer.validated_data.get('description')
        print(description)
        if not description:
            description= f'None description of the book {name}'
        serializer.save(description= description)

        return Response(serializer.data)

#Thi APIview will look for all the books the book that has the lookuo_field pk and update that information
class BookUpdateAPIView(UpdateAPIView):
    queryset= Book.objects.all()
    serializer_class = BookSerializerUpdate
    lookup_field = 'pk'
    permission_classes= [SraffEditorPermissionMixin]

    #This function will be called when the object will update so you can handle some more logic when updating the object
    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data)
    

#THis class will destroy the caertain object with the certain pk
# class BookDestroyApiView(DestroyAPIView):
#     queryset= Book.objects.all()
#     serializer_class = BookSerializerUpdate
#     lookup_field = 'pk'
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes= [permissions.DjangoModelPermissions]

#     def perform_destroy(self, instance):
#         return super().perform_destroy(instance)
    
#We are mixing all the http method in one clas   #The best choice
class BookMixinView(
    mixins.DestroyModelMixin,
    UserQuerySetMixin,
    mixins.ListModelMixin,  #This will add all the CRUD get(), POST() , etc ...
    mixins.RetrieveModelMixin, #This will help us to search certain objects  add the lookup_field
    mixins.CreateModelMixin,
    GenericAPIView
    ):
    queryset= Book.objects.all()
    serializer_class= BookSerializer
    lookup_field = 'pk'
    permission_classes= [SraffEditorPermissionMixin]  #all class views that is imported from Generics can have this atribute permission_classes
                        #I add a custom model permission so only the staff that has the permission can see the data << permission.py >>

    def get(self,request,**kwargs): #HTTP --> GET
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request)  #The mixins.RetrieveModelMixin provides the retrieve that with the pk search for an object of the queryset
        return self.list(request,kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) # The mixins.CreateModelMixin add the create to the self so it will automatically with the POst.data will create a new Book object

    # <<  If you want to do some logic when you want to create an object you can add this function to do some more things >>
    
    def perform_create(self, serializer):
        try:
            email = serializer.validated_data.pop('email')
            print(email)
        except: 
            pass
        serializer.save(user= self.request.user)
        return Response(serializer.data)
    
    def delete(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.destroy(request, *args, **kwargs)
        return Response({'Error':'pk mission or does not exist'})
    

# class BookList(ListAPIView):
#     serializer_class = BookSerializerSearch
#     def get_queryset(self):
#         queryset= Book.objects.all()
#         search = self.kwargs['search']

#         if search == 'all':
#             queryset = queryset.filter((Q(existence=True) | Q(user=self.request.user)))
#         elif search is not None:
#             queryset = queryset.filter(
#                 (Q(user__username__icontains=search) | Q(description__icontains=search) | Q(author__name__icontains=search) ) & (Q(existence=True) | Q(user=self.request.user))
#             )

#         else:
#             queryset=Book.objects.none()
#         return queryset
    
class BookList(GenericAPIView):
    def get(self,request,*args,**kwargs):
        user = request.GET.get('user') if (request.GET.get('user') and request.user.is_authenticated) else None
        print(user)
        query=request.GET.get('q')   #Here is q cause when you search like this example http://127.0.0.1:8000/api/books/?q=to    it will retrieve tha valuee of q and the value of q is to
        tag = request.GET.get('tag') or None
        existence = bool(request.GET.get('existence')) if request.GET.get('existence') else None
        if not query:
            return Response('', status=400)
        results = client.perform_search(query,tags = tag, existence=existence, user =user)   #We are using the fucntions of client.py 
        return Response(results)


        

        
        

