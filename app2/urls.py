from django.urls import path
from . import views

urlpatterns=[
    path('book/',views.book_alt_view),
    path('book/<int:pk>/',views.book_alt_view)
]