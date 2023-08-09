from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from core.forms import SignupForm, LoginForm, PostForm, AddProfileForm, CommentForm, ArticlePostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment, ArticlePost
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse



# Create your views here.

# function based view for SignupForm
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user=fm.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect('sign-up')
        else:
            messages.error(request, 'Form data is not Valid!')
    else:
        fm = SignupForm() 
    context = {'form':fm}
    return render(request, "core/signup.html", context)
  

# function based view for login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        fm = LoginForm(request=request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')      
    else:
        fm = LoginForm()
    context = {'form':fm}
    return render(request, "core/login.html", context)

#function based view for index page
def index_view(request):
    if request.user.is_authenticated:
        post_id = request.GET.get('post_id')  # Get the post_id from the query parameters

        if request.method == "POST":
            fm = PostForm(request.POST, request.FILES)
            if fm.is_valid():
                content_text = fm.cleaned_data['content_text']
                content_image = fm.cleaned_data['content_image']
                content_file = fm.cleaned_data['content_file']
                post = None

                if content_text and content_image:
                    post = Post(content_text=content_text, content_image=content_image, creator=request.user)
                elif content_text and content_file:
                    post = Post(content_text=content_text, content_file=content_file, creator=request.user)                   
                elif content_text:
                    post = Post(content_text=content_text, creator=request.user)
                elif content_image:
                    post = Post(content_image=content_image, creator=request.user)
                elif content_file:
                    post = Post(content_file=content_file, creator=request.user)


                if post:
                    post.save()
                    messages.success(request, "Your Post has been uploaded Successfully!")
                    return redirect('index')
        else:
            fm = PostForm()
            all_posts = Post.objects.all().order_by('-date_created').select_related('creator__profile')

            #profile
            profile = Profile.objects.get(user=request.user)

            #suggestion
            suggestion = Profile.objects.exclude(user=request.user)[0:5]
           
            #paginator
            paginator = Paginator(all_posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)


        context = {'form':fm,'posts':page_obj, 'user_profile':profile, 'suggestion':suggestion, 'post_id':post_id}
        return render(request, "core/index.html", context)
    else:
        return redirect('log-in')
    
# function based view for logout
@login_required(login_url='log-in')
def logout_view(request):
    logout(request)
    return redirect('log-in')

#unction based view for profile
@login_required(login_url='log-in')
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        fm = AddProfileForm(request.POST, request.FILES, instance=profile)
        if fm.is_valid():
            profile = fm.save(commit=False)
            profile.user = request.user  # Assuming you have a user associated with the profile
            profile.save()
            return redirect('profile')  # Replace 'profile' with the URL name of your profile page
    else:
        fm = AddProfileForm()       
        profile = Profile.objects.get(user=request.user)
        post_count = profile.get_post_count()
        suggestion = Profile.objects.exclude(user=request.user)      
        posts = Post.objects.filter(creator=request.user).order_by('-date_created').select_related('creator__profile')

    context = {'form':fm, 'profile':profile, 'posts':posts, 'user_profile':profile, 'suggestion':suggestion, 'post_count':post_count}
    return render(request, "core/profile.html", context)

# function based view for user profile 
@login_required(login_url='log-in')
def user_profile_view(request, profile_id=None, user_id=None):
    logged_profile = Profile.objects.get(user=request.user)
    suggestion = Profile.objects.exclude(user=request.user)

    if profile_id:
        current_profile = get_object_or_404(Profile, id=profile_id)
        current_user = current_profile.user
    elif user_id:
        current_user = get_object_or_404(User, id=user_id)
        current_profile = Profile.objects.get(user=current_user)
    else:
        return HttpResponse("Invalid request")

    current_posts = Post.objects.filter(creator=current_user).order_by('-date_created').select_related('creator__profile')
    post_count = current_profile.get_post_count()

    context = {
        'profile': current_profile,
        'posts': current_posts,
        'user_profile': logged_profile,
        'suggestion': suggestion,
        'post_count': post_count
    }

    return render(request, "core/user_profile.html", context)

# function based view for search user
def search_view(request):
    search = request.GET.get('username', '')
    profiles = None

    if search:
        profiles = Profile.objects.filter(user__username__icontains=search)

    context = {'profiles':profiles, 'search':search}
    return render(request, "core/search.html", context)

# function based view for updating post
@login_required(login_url='log-in')
def edit_post_view(request, post_id):
    if request.method=="POST":
        current_post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, request.FILES, instance=current_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('profile')
    else:
        current_post = Post.objects.get(id=post_id)
        form = PostForm(instance=current_post)

    context = {'form':form}
    return render(request, "core/updatepost.html", context)

# function based view for deleting post
@login_required(login_url='log-in')
def delete_post_view(request, post_id):
    if request.method == "POST":
        target_post = Post.objects.get(id=post_id)
        target_post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('profile')
    
#function based view for following users
def follow_unfollow_view(request, profile_id=None, user_id=None):
    if profile_id:
        current_profile = Profile.objects.get(id=profile_id)
        logged_profile = Profile.objects.get(user=request.user)

        if request.user in current_profile.followers.all():
            current_profile.followers.remove(request.user)
            logged_profile.followings.remove(current_profile.user)
        else:
            current_profile.followers.add(request.user)
            logged_profile.followings.add(current_profile.user)

        redirect_url = reverse('suggestion-profile', kwargs={'profile_id': profile_id})
        return redirect(redirect_url)

    elif user_id:
        current_user = User.objects.get(id=user_id)
        current_profile = Profile.objects.get(user=current_user)
        logged_profile = Profile.objects.get(user=request.user)
        
        if request.user in current_profile.followers.all():
            current_profile.followers.remove(request.user)
            logged_profile.followings.remove(current_profile.user)
        else:
            current_profile.followers.add(request.user)
            logged_profile.followings.add(current_profile.user)
        
        return redirect('index')     #redirect to the home page
    else:
        return HttpResponse("Page Not found")
    
# function based view for like the post
@login_required(login_url='log-in')
def like_post_view(request, post_id=None):
    current_post = Post.objects.filter(id=post_id)
        
    if request.user in current_post[0].likers.all():
        current_post[0].likers.remove(request.user)
    else:
        current_post[0].likers.add(request.user)

    return redirect('index')


#function based view for saving post
@login_required(login_url='log-in')
def save_post_view(request, post_id=None):
    current_post = Post.objects.filter(id=post_id)

    if request.user in current_post[0].savers.all():
        current_post[0].savers.remove(request.user)
    else:
        current_post[0].savers.add(request.user)

    # Generate the URL for the index page
    url = reverse('index')

    # Append the post_id as a query parameter
    url = f'{url}?post_id={post_id}'

    return redirect(url)


#function based view for commenting in post
@login_required(login_url='log-in')
def add_comment_view(request, post_id):
    current_post = get_object_or_404(Post, id=post_id)
    comments = current_post.comments.all().order_by('-date_created')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            commenter = request.user
            comment = Comment.objects.create(post=current_post, commenter=commenter, comment_text=comment_text)
            current_post.comments.add(comment)
            return redirect('add-comment', post_id=post_id)
    else:
        form = CommentForm()
    
    context = {'form':form, 'post':current_post, 'comments':comments}

    return render(request, 'core/add_comment.html', context) 


# function based view for chatting functionality
@login_required(login_url='log-in')
def chatting_view(request):
    logged_profile = Profile.objects.get(user=request.user)
    context = {'user_profile':logged_profile}
    return render(request, "core/chatting.html", context)


# function based view for ArticlePost
@csrf_exempt
def article_post_view(request):

    logged_profile = Profile.objects.get(user=request.user) # for displaying profile_pic of logged user
    suggestion = Profile.objects.exclude(user=request.user) #for displaying suggestions list

    
    articles_list = ArticlePost.objects.all().order_by('-date_created')

    context = {'user_profile':logged_profile, 'posts':articles_list, 'suggestion':suggestion}

    return render(request, "core/article.html", context)


@login_required(login_url='log-in')
def create_article_view(request):
    if request.method == "POST":
        form = ArticlePostForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.art_maker = request.user
            article.date_created = timezone.now()
            article.save()

            messages.success(request, 'Your Article has been created!')
            return redirect('articles')
    else:
        form = ArticlePostForm()

    context = {'fm':form,}
    return render(request, "core/create_article.html", context)

# function based view for detailed artile of particular id
@login_required(login_url='log-in')
def detail_article_view(request, article_id=None):
    if article_id:
        current_article = ArticlePost.objects.get(id=article_id)
    else:
        messages.info(request, 'No Article to show')
    
    context = {'current_article':current_article}
    
    return render(request, "core/detailArticle.html", context)


#function based view for deleting article
@login_required(login_url='log-in')
def delete_article_view(request, del_article_id=None):
    if del_article_id:
        current_article = ArticlePost.objects.get(id=del_article_id)
        if current_article.art_maker == request.user:
            current_article.delete()
            messages.success(request, "Article Deleted Successfully!")
            return redirect('articles')
        else:
            messages.error(request, "You are not allowed to delete others articles!")
            return redirect('articles')
    else:
        messages.info(request, 'No Articles Found!')


# function based view for about_us section
def about_us_view(request):
    return render (request, "core/about_us.html")

    
