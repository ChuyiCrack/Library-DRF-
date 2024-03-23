from django.urls import path,re_path
from rest_framework import routers
from .views import Books,Index,BookDetailAPIView,BookCreateAPIView,BookUpdateAPIView,BookMixinView,BookList
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns=[
    path('auth/', obtain_auth_token),
    path('',Index.as_view()),
    path('book/',Books, name='book'),
    path('all_books/',BookMixinView.as_view(),name='all_books'),
    path('book/<int:pk>/', BookMixinView.as_view(), name='book_detail'),
    path('book/create/', BookMixinView.as_view()),
    path('book/<int:pk>/update/', BookUpdateAPIView.as_view(), name='Book-Edit'),
    path('book/<int:pk>/destroy/',BookMixinView.as_view()),
    

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),         
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # all this is for JWT part of the tutorial    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),           
    
    
    #re_path("^books/(?P<search>\w+)/$", BookList.as_view()),
    path("books/", BookList.as_view())
]