from django.shortcuts import render, redirect, get_object_or_404
from .models import Publisher, Article
from django.contrib.auth.models import User, Group
from .forms import RegisterForm, LoginUserForm, ArticleForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import tweepy
from django.conf import settings

Reader, created = Group.objects.get_or_create(name='Reader')
Journalist, created = Group.objects.get_or_create(name='Journalist')
Editor, created = Group.objects.get_or_create(name='Editor')

# Create your views here.
def frontpage_view(request):
    publisher_list = Publisher.objects.all()
    context = {'publisher_list': publisher_list}
    return render(request, "news/frontpage.html", context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_group = form.cleaned_data['user_type']
            if user_group == "EDITOR":
                my_group = Group.objects.get(name='Editor')
                new_user = form.save(commit=False)
                new_user.save()
                new_user.userprofile.user_type = user_group
                new_user.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1']
                                        )
                login(request, new_user)
                my_group.user_set.add(request.user)
                return redirect('news:frontpage')
            elif user_group == 'READER':
                my_group = Group.objects.get(name='Reader')
                new_user = form.save(commit=False)
                new_user.save()
                new_user.userprofile.user_type = user_group
                new_user.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1']
                                        )
                login(request, new_user)
                my_group.user_set.add(request.user)
                return redirect('news:frontpage')
            elif user_group == 'JOURNALIST':
                my_group = Group.objects.get(name='Journalist')
                new_user = form.save(commit=False)
                new_user.save()
                new_user.userprofile.user_type = user_group
                new_user.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1']
                                        )
                login(request, new_user)
                my_group.user_set.add(request.user)
                return redirect('news:frontpage')
    else:
        form = RegisterForm()
    return render(request, "news/register.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('news:frontpage'))
    else:
        form = LoginUserForm()
    return render(request, "news/login.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('news:frontpage')


def publisher_details_view(request, pk):
    user = request.user
    Journalist = user.groups.filter(name='Journalist').exists()
    editor = user.groups.filter(name='Editor').exists()
    publisher = get_object_or_404(Publisher, pk=pk)
    publisher_articles = Article.objects.filter(publisher=publisher)
    context = {
        'Journalist': Journalist,
        'editor': editor,
        'user': user,
        'publisher': publisher,
        'publisher_articles': publisher_articles,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            current_user_profile = request.user.userprofile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows_publisher.remove(publisher.pk)
            elif action == 'follow':
                current_user_profile.follows_publisher.add(publisher.pk)
            current_user_profile.save()
    return render(request, "news/publisher_details.html", context)


def add_article_view(request, pk):
    user = request.user
    if user.has_perm('news.add_article'):
        if request.method == "POST":
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.publisher = Publisher.objects.get(pk=pk)
                article.journalist = request.user
                article.save()
                return redirect("news:frontpage")
        else:
            form = ArticleForm()
        return render(request, "news/add_article.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('news:frontpage'))
    

def update_article_view(request, pk):
    user = request.user
    if user.has_perm('news.change_article'):
        article = get_object_or_404(Article, pk=pk)
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form = form.save(commit=False)
                article.approved = True
                form.save()
                return redirect("store:frontpage")
        else:
            form = ArticleForm(instance=article)
        return render(request, "news/add_article.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('news:frontpage'))
    

def delete_article_view(request, pk):
    user = request.user
    if user.has_perm('news.delete_article'):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect("news:frontpage")
    else:
        return HttpResponseRedirect(reverse('news:frontpage'))
    

def edit_article_view(request, pk):
    user = request.user
    if user.has_perm('news.change_article'):
        article = get_object_or_404(Article, pk=pk)
        if request.method == "POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.save()
                return redirect("news:frontpage")
        else:
            form = ArticleForm(instance=article)
        return render(request, "news/add_article.html", {"form": form})
    else:
        return HttpResponseRedirect(reverse('news:frontpage'))


def article_details_view(request, pk):
    user = request.user
    editor = user.groups.filter(name='Editor').exists()
    article = get_object_or_404(Article, pk=pk)
    context ={
        'article': article,
        'editor': editor,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            action = request.POST['approve']
            if action == 'approve':
                article.approved = True
            elif action == 'unapprove':
                article.approved = False
            article.save()
    return render(request, "news/article_details.html", context)


def user_profile_view(request, pk):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, pk=pk)
        profile = profile_user.userprofile
        context = {
        'profile': profile, }
        if request.method == "POST":
            current_user_profile = request.user.userprofile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows_user.remove(profile)
            elif action == 'follow':
                current_user_profile.follows_user.add(profile)
            current_user_profile.save()

        return render(request, "news/profile.html", context)


@receiver(post_save, sender=Article,)
def send_email(sender, instance: Article, **kwargs):
    article = Article.objects.get(pk=instance.pk)
    journalist = article.journalist
    publisher = article.publisher
    if article.approved == True:
        journalist_sub_users = User.objects.get(follows_user=journalist)
        for user in journalist_sub_users:
            user_email = user.email
            send_mail(
                'New artricle',
                'A new article has been published',
                'news_app@gmail.com',
                [f'{user_email}'],
            )
        publisher_sub_user = User.objects.get(follows_publisher=publisher)
        for user in publisher_sub_user:
            user_email = user.email
            send_mail(
                'New artricle',
                'A new article has been published',
                'news_app@gmail.com',
                [f'{user_email}'],
            )


@receiver(post_save, sender=Article,)
def send_tweet(sender, instance: Article, **kwargs):
    article = Article.objects.get(pk=instance.pk)
    if article.approved == True:
        journalist = article.journalist
        auth = tweepy.OAuth1UserHandler(settings.API_KEY, settings.API_KEY_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.update_status(f'{article.title} has been posted by {journalist}')