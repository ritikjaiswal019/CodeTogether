from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blogHome, name="blogHome"),
    path('search',views.search, name="search"),
    path('postComment', views.postComment, name="postComment"),
    path('<str:slug>', views.viewBlog, name="viewBlog"),
]