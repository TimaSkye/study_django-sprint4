from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView
)

from .constants import PAGINATE_COUNT
from .forms import ProfileForm, CommentForm, PostCreateForm
from .mixins import OnlyAuthorMixin, CommentMixin
from .models import Post, Category, User, Comment
from .utils import get_filter_query


class IndexView(ListView):
    """CBV списка постов."""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = PAGINATE_COUNT
    ordering = ['-pub_date']

    def get_queryset(self):
        return get_filter_query(Post.objects).order_by('-pub_date')


class ProfileView(TemplateView):
    """CBV Профиля пользователя."""

    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        profile = get_object_or_404(User, username=username)
        if profile == self.request.user:
            posts = Post.objects.filter(author=profile).order_by(
                '-pub_date').annotate(comment_count=Count('comments'))
        else:
            posts = get_filter_query(Post.objects, author=profile).order_by(
                '-pub_date')

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['profile'] = profile
        context['page_obj'] = page_obj
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """CBV редактирования профиля пользователя."""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostView(DetailView):
    """CBV детального отображения поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            user_posts = Q(author=self.request.user)
            published_posts = Q(is_published=True,
                                pub_date__lte=timezone.now(),
                                category__is_published=True)
            return queryset.filter(
                user_posts | published_posts).select_related(
                'author').prefetch_related('category', 'location', 'comments')

        return get_filter_query(queryset).select_related(
            'author').prefetch_related('category', 'location', 'comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('created_at')
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


class CategoryPostsView(ListView):
    """CBV категорий постов."""

    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category_posts'
    paginate_by = PAGINATE_COUNT

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(Category, slug=category_slug,
                                          is_published=True)
        return Post.published.filter(category=self.category).annotate(
            comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV создание поста."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', kwargs={'username': username})


class PostEditView(OnlyAuthorMixin, UpdateView):
    """CBV редактирования поста."""

    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        if not self.test_func():
            return redirect(reverse(
                'blog:post_detail',
                kwargs={'post_id': self.kwargs['post_id']}))
        return None

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    """CBV удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    """CBV добавления комментария."""

    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse('blog:post_detail',
                       kwargs={'post_id': post_id})

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(CommentMixin, UpdateView):
    """CBV редактирования комментария."""

    form_class = CommentForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context


class CommentDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    """CBV удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context
