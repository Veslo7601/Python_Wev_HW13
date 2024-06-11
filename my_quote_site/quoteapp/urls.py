from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag_create, name='tag'),
    path('author/', views.author_create, name='author'),
    path('quote/', views.quote_create, name='quote'),
    path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
]