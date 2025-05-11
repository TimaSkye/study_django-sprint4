from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, \
    DeleteView

from blog.forms import PostForm, UserForm
from blog.models import Post, Category, User


class ProfileView(View):
    """CBV Профиля пользователя."""
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get(self, request, username):
        profile = get_object_or_404(User, username=username)
        posts_list = profile.posts.all().order_by('-pub_date')

        paginator = Paginator(posts_list, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'profile': profile,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    """CBV редактирования профиля пользователя."""
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


def post_detail(request, post_id: int):
    """Страница с подробной информацией о посте."""
    post = get_object_or_404(Post.published, pk=post_id)
    return render(request, 'blog/detail.html',
                  {'post': post})


class CategoryPostsView(ListView):
    """CBV категорий постов."""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category_posts'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(Category, slug=category_slug,
                                          is_published=True)
        return Post.published.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем объект категории в контекст
        context['category'] = self.category
        return context


class PostDetailView(DetailView):
    """CBV поста."""
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'


class PostListView(ListView):
    """CBV списка постов."""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-pub_date']


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV создание поста."""
    model = Post
    form_class = PostForm
    exclude = ['author']
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        """метод назначения авторства."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    pass


class PostDeleteView(LoginRequiredMixin, DeleteView):
    pass


class CommentCreateView(LoginRequiredMixin, CreateView):
    pass
