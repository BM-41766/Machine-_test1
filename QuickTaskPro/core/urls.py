from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import UserViewSet, OrganizationViewSet
from tasks.views import ProjectViewSet, TaskViewSet

# Initialize the router
router = routers.DefaultRouter()

# Register all viewsets with the router
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include router URLs - this should come FIRST
    path('api/', include(router.urls)),
    
    # Include app-specific URLs (only if you have additional custom endpoints)
    path('api/accounts/', include('accounts.urls')),  # Only if you have extra account endpoints
    path('api/tasks/', include('tasks.urls')),  # Only if you have extra task endpoints
]