from django.urls import path
from posts import views
from users import views as user_views 

from posts.views import (
PostDetailView, PostCreateView, PostUpdateView,
PostDeleteView, UserDetailView)

urlpatterns = [
    path('', views.showPost, name='posts-home'),
    path('post/<slug>/', views.PostDetailView , name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('search/', views.search, name='search'),
    path('alluser/', user_views.showAllUser, name='alluser'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]


