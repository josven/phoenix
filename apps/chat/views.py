from models import *
from forms import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login/')
def chat(request):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            results = "valid"
        else:
            results = "invalid"
    else:
        results = "get"
        form = PostForm()
    
    posts = Post.objects.order_by('-date_created')[:10]

    return render(request,'chat.html', {"results": results,"form":form,"posts":posts})