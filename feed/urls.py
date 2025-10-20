from django.urls import path
from . import views

app_name = 'feed' 

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('create/', views.create_post, name='create_post'),
    path('friends/', views.friends_feed, name='friends_feed'), 
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path("subscriptions/", views.subscriptions_feed, name="subscriptions_feed"),

]
