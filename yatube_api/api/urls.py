from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet)
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments'
                   )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    # path("v1/", include("djoser.urls.jwt"))
    re_path("v1/jwt/create/",
            views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path("v1/jwt/refresh/",
            views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path("v1/jwt/verify/",
            views.TokenVerifyView.as_view(), name="jwt-verify"),
]
