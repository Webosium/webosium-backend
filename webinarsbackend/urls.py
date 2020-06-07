from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
import rest_framework_social_oauth2.urls

from core import views 

from rest_framework import routers
from core.views import *

router = routers.DefaultRouter()
router.register('events/all', EventAllApiViewSet, basename='events_all')
router.register('events/user', EventUserApiViewSet, basename='events_user')
router.register('events', EventApiViewSet, basename='events_create')

router.register('tags/all', TagAllApiViewSet, basename='tags_all')
router.register('tags', TagApiViewSet, basename='tags_create')

router.register('fests/overview', FestOverviewApiViewSet, basename='fests_overview')
router.register('fests/details', FestDetailsApiViewSet, basename='fests_details')
router.register('fests/create', FestCreateApiViewSet, basename='fests_create')


# router.register('user', UserCreateAPIView, basename='user_new'),
router.register('userinfo', UserInfoAPIView, basename='user_info'),

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', obtain_auth_token, name='rest-api-auth'),
    path('api/api-auth/', include('rest_framework.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)