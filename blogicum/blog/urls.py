from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'
         ),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),
    path('posts/<int:post_id>/comment',
         views.AddCommentView.as_view(),
         name='add_comment'
         ),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         views.EditCommentView.as_view(),
         name='edit_comment'
         ),
    path('posts/<post_id>/delete_comment/<comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         ),
    path('posts/<int:post_id>/edit/',
         views.PostEditView.as_view(),
         name='edit_post'
         ),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),
    path('posts/<int:post_id>/',
         views.PostView.as_view(),
         name='post_detail'
         ),
    path('category/<slug:category_slug>/',
         views.CategoryPostsView.as_view(),
         name='category_posts'
         ),
    path('profile/<str:username>/',
         views.ProfileView.as_view(),
         name='profile'
         ),
    path('edit_profile/',
         views.EditProfileView.as_view(),
         name='edit_profile'
         ),
]
