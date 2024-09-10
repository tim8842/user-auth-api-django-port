from django.urls import path
from .views import RegisterView, LoginView, ChangePasswordView, UpdateProfileView, ProfileDetailView

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('sentry-debug/', trigger_error),
]
