from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', auth_views.UserProfileView.as_view(), name='user_profile'),
    path('change-password/', auth_views.ChangePasswordView.as_view(), name='change_password'),
    path('upload-avatar/', auth_views.UploadAvatarView.as_view(), name='upload_avatar'),
]
