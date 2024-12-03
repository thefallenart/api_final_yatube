from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
)
from posts.models import Group, Post


class CreateListGenericViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    '''Вьюсет получает записи, изменения и удаления постов.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Создает запись, где автором является пользователем из запроса."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет получает данные групп пользователей.'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет получает записи и изменения комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущей поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        """
        Создает комментарий для поста с id,
        где автором является пользователь из запроса.
        """
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(CreateListGenericViewSet):
    """Вьюсет для обьектов модели Follow."""
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращает queryset c подписками для пользователя из запроса."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Создает подписку, где подписчиком является пользователь из запроса.
        """
        serializer.save(user=self.request.user)
