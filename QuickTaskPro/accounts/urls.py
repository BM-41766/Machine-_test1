from django.urls import path
from .views import OrganizationListCreateView, UserRegistrationView, UserListView, UserDetailView

urlpatterns = [
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]