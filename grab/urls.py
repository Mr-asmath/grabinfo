from django.urls import path
from . import views
urlpatterns=[
  path('',views.home,name='home'),
  path('explore/', views.explore, name='explore'),
  path('moments/', views.moments, name='moments'),
  path('activity/', views.activity, name='activity'),
  path('inbox/', views.inbox, name='inbox'),
  path('saved/', views.saved_posts, name='saved_posts'),
  path('signup',views.signup,name="signup"),
  path('login',views.login_page,name="login"),
  path('logout',views.logout_page,name="logout"),
  path('profile/', views.profile, name='profile'),
  path('profile/delete/<int:id>/',views.delete,name='delete'),
  path('profile/<int:id>/', views.profile_view, name='profile_view'),
  path('profile/<int:id>/followers/', views.followers_list, name='followers_list'),
  path('profile/<int:id>/following/', views.following_list, name='following_list'),
  path('profile/<int:id>/follow/', views.toggle_follow, name='toggle_follow'),
  path('profile_edit/', views.profile_edit, name='profile_edit'),
  path('posts/new/', views.create_post, name='post_create'),
  path('posts/<int:id>/like/', views.toggle_like, name='toggle_like'),
  path('posts/<int:id>/save/', views.toggle_save, name='toggle_save'),
  path('posts/<int:id>/comment/', views.add_comment, name='add_comment'),
  path('search',views.search_profile,name="searchs"),

  # New social media style pages
  path('notifications/', views.notifications, name='notifications'),
  path('messages/', views.messages, name='messages'),
  path('friends/', views.friends, name='friends'),
]
