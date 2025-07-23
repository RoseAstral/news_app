from django.urls import path
from .views import (
    frontpage_view,
    register_view,
    login_view,
    logout_view,
    publisher_details_view,
    add_article_view,
    delete_article_view,
    edit_article_view,
    article_details_view,
    user_profile_view,
)

app_name = "news"
urlpatterns = [
    path("", frontpage_view, name="frontpage"),

    path("register/",  register_view, name="register"),
   
    path("login/", login_view, name="login"),

    path('logout/', logout_view, name='logout'),

    path('publisher_details/<int:pk>/', publisher_details_view, name="publisher_details"),
    
    path('publisher_details/<int:pk>/add_article/', add_article_view, name='add_article'),
    
    path('delete_article/<int:pk>/', delete_article_view, name='delete_article'),

    path('edit_article/<int:pk>/', edit_article_view, name="edit_article"),

    path('article_details/<int:pk>/', article_details_view, name='article_details'),

    path('profile/<int:pk>/', user_profile_view, name='view_profile'),
]