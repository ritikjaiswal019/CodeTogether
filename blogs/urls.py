from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.blogHome, name="blogHome"),
    path('search',views.search, name="search"),
    path('postComment', csrf_exempt(views.postComment), name="postComment"),
    path('createblog', views.createBlog, name="createBlog"),
    path('likeunlike', csrf_exempt(views.likeunlike), name="likeunlike"),
    path('<str:slug>', views.viewBlog, name="viewBlog"),
]