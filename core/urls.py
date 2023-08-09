from django.urls import path
from core import views

urlpatterns = [
    path('', views.login_view, name="log-in"),
    path('signup/', views.signup_view, name="sign-up"),
    path('homepage/', views.index_view, name="index"),
    path('logout/', views.logout_view, name="log-out"),
    path('profile/', views.profile_view, name="profile"),
    path('userProfile/<int:user_id>/', views.user_profile_view, name="user-profile"),
    path('suggestionProfile/<int:profile_id>/', views.user_profile_view, name="suggestion-profile"),
    path('searchProfile/<int:profile_id>/', views.user_profile_view, name="search-profile"),
    path('search/', views.search_view, name="search"),
    path('delete_post/<int:post_id>/', views.delete_post_view, name="delete-post"),
    path('update_post/<int:post_id>/', views.edit_post_view, name="update-post"),
    path('follow_unfollow/<int:profile_id>/', views.follow_unfollow_view, name="follow-unfollow"),
    path('follow_unfollow_user/<int:user_id>/', views.follow_unfollow_view, name="follow-unfollow-user"),
    path('like_post/<int:post_id>/', views.like_post_view, name="like-post"),
    path('save_post/<int:post_id>/', views.save_post_view, name="save-post"),
    path('add_comment/<int:post_id>/comment/', views.add_comment_view, name='add-comment'),
    path('chatting/', views.chatting_view, name="chat-user"),
    path('articles/', views.article_post_view, name="articles"),
    path('create_article/', views.create_article_view, name="create-article"),
    path('detail_article/<int:article_id>/', views.detail_article_view, name='detail-article'),
    path('delete_article/<int:del_article_id>/', views.delete_article_view, name="delete-article"),
    path('about_us/', views.about_us_view, name="about-us"),


]
