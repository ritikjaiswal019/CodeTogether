from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from blogs.templatetags import extras
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
import json

# Create your views here.
allPosts = Post.objects.all()

def blogHome(request):
    popularPosts = Post.objects.annotate(likecount=Count('likes')).order_by('-likecount')[:4]
    return render(request, 'blogs/index.html',{
        "blogs":allPosts,'popularposts': popularPosts
    })

def search(request):
    query=request.GET['searchqry']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    if len(query)==0:
        messages.warning(request, "Please type something to search")
        allPosts = Post.objects.none()
    
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'blogs/search.html', params)

def viewBlog(request, slug):
    if allPosts.filter(slug=slug).exists():
        cuser = request.user
        post=Post.objects.filter(slug=slug).first()
        comments= BlogComment.objects.filter(post=post, parent=None)
        replies= BlogComment.objects.filter(post=post).exclude(parent=None)
        popularPosts = Post.objects.annotate(likecount=Count('likes')).order_by('-likecount')[:4]
        replyDict={}
        liked = False
        if post.likes.all().filter(username=cuser.username).exists():
            liked = True
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        context={'blog':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict, 'liked': liked, 'popularposts': popularPosts}
        return render(request, "blogs/view_blog.html", context)
    else:
        messages.error(request, 'No Such Blog Exist')
        return redirect('blogHome')

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno==None:
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blogs/{post.slug}")

def createBlog(request):
    return render(request, 'blogs/create_blog.html')

def likeunlike(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cuser = request.user
        blo = data['blno']
        post = Post.objects.get(sno=blo)
        alreadyliked = False
        if post.likes.all().filter(username=cuser.username).exists():
            alreadyliked=True
        if alreadyliked:
            alllikes = post.likes.all().exclude(username=cuser.username)
            post.likes.set(alllikes)
            post.save()
            return JsonResponse({'isLikedTrue':'False'})
        else:
            post.likes.add(cuser.pk)
            return JsonResponse({'isLikedTrue':'True'})