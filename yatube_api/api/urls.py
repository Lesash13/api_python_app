from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register('posts', views.PostViewSet, basename='posts')
router_v1.register('groups', views.GroupsViewSet, basename='groups')
router_v1.register('follow', views.FollowViewSet, basename='follow')

router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')
urlpatterns = [
    path('v1/', include(router_v1.urls), name='posts-v1'),
    path('v1/api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
