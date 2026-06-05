from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book-session/', views.book_session, name='book_session'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('give/', views.give, name='give'),
    path('about/', views.about, name='about'),
]