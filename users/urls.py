from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView, UpdateProfileView, ProfileDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
]
