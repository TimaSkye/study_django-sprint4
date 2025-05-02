from django.shortcuts import render, get_object_or_404

from blog.constants import POSTS_ON_PAGE
from blog.models import Post, Category


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
