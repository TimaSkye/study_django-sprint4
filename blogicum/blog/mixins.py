from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied(
            'Вы не авторизованы для удаления этого комментария.')


class CommentMixin(LoginRequiredMixin, OnlyAuthorMixin):
    model = Comment
    template_name = 'blog/comment.html'
