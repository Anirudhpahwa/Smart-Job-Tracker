from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobApplicationViewSet
from analytics.views import UserAnalyticsView, RecomputeAnalyticsView

router = DefaultRouter()
router.register(r'jobs', JobApplicationViewSet, basename='job')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/analytics/', UserAnalyticsView.as_view(), name='analytics'),
    path('api/v1/analytics/recompute/', RecomputeAnalyticsView.as_view(), name='recompute_analytics'),
]
