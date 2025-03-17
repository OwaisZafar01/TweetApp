from django.shortcuts import render
from tweet.models import Tweet
from tweet.forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.

def index(request):
    return render(request,'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('created_at')

    return render(request, 'tweet_list.html',{'tweets':tweets})

@login_required(login_url='/accounts/login/?next=/tweet/create/')
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user    # Link the tweet to the logged-in user
            tweet.save()
            return redirect('tweet_list')   #So the user can see their new tweet along with others.
        
    else:
        form = TweetForm()

    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request , tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES,instance=tweet)  # Prefill the form with existing tweet data
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user                   # Link the tweet to the logged-in user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm(instance = tweet)

    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})
    


def register(request):  
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup

            next_url = request.GET.get('next', 'tweet_list')  # Check if redirect URL exists
            return redirect(next_url)


              # Redirect to tweets page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})




