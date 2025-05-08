from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from blog.constants import POSTS_ON_PAGE
from blog.forms import UserEditForm
from blog.models import Post, Category, User


def index(request):
    """Главная страница с последними опубликованными постами."""
    post_list = Post.published.all()[:POSTS_ON_PAGE]
    return render(request, 'blog/index.html',
                  {'post_list': post_list})


def post_detail(request, post_id: int):
    """Страница с подробной информацией о посте."""
    post = get_object_or_404(Post.published, pk=post_id)
    return render(request, 'blog/detail.html',
                  {'post': post})


def category_posts(request, category_slug: str):
    """Страница с постами определённой категории."""
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = Post.published.filter(category=category)
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'category_posts': posts,
        },
    )


def create_post():
    return None


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.all().order_by('-created_at')

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'blog/user.html',
                  {'form': form})
