from django.shortcuts import render, HttpResponse, redirect
from .models import Post

from django.contrib import messages

# Create your views here.
allPosts = Post.objects.all()

def blogHome(request):
    return render(request, 'blogs/index.html',{
        "blogs":allPosts
    })

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        # allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'blogs/search.html', params)

def viewBlog(request, slug):
    if allPosts.filter(slug=slug).exists():
        post = allPosts.get(slug=slug)
        return render(request, 'blogs/view_blog.html',{
            "blog":post,
        })
    else:
        messages.error(request, 'No Such Blog Exist')
        return redirect('blogHome')
