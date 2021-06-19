from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from blogs.templatetags import extras
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
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'blogs/search.html', params)

def viewBlog(request, slug):
    if allPosts.filter(slug=slug).exists():
        post=Post.objects.filter(slug=slug).first()
        comments= BlogComment.objects.filter(post=post, parent=None)
        replies= BlogComment.objects.filter(post=post).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)
        context={'blog':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
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