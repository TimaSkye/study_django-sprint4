from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(),
         name='index'),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(),
         name='category_posts'),
    path('profile/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(),
         name='edit_profile'),
]
