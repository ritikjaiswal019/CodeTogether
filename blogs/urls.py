from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blogHome, name="blogHome"),
    path('search',views.search, name="search"),
    path('<str:slug>', views.viewBlog, name="viewBlog"),
]