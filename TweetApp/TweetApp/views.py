
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from tweet.models import Tweet



def home(request):
    if request.user.is_authenticated:  
        logout(request)
    tweets = Tweet.objects.all().order_by('created_at')  
    return render(request, 'tweet_list.html', {'tweets': tweets})