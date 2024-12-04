from django.urls import path
from accounts.views import RegisterView, CustomTokenObtainPairView, AdminOnlyView, ModeratorOnlyView, AdminOrModeratorView, UserOnlyView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import register_view, login_view, admin_view, user_view, logout_view, admin_moderator_view,drf

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # API
    path('register-fron/', register_view, name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # API
    path('login-fron/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # API
    path('admin-view/', AdminOnlyView.as_view(), name='admin_view'),# API
    path('admin-view-fron/', admin_view, name='admin_view_fron'),
    path('moderator-view/', ModeratorOnlyView.as_view(), name='moderator_view'),# API
    path('admin-or-moderator-view/', AdminOrModeratorView.as_view(), name='admin_or_moderator_view'),# API
    path('admin-moderator-view-fron/', admin_moderator_view, name='admin_moderator_view_fron'),
    path('user-view/', UserOnlyView.as_view(), name='user_view'),# API
    path('user-view-fron/', user_view, name='user_view_fron'),
    path('logout/', LogoutView.as_view(), name='logout_api'),# API
    path('logout-fron/', logout_view, name='logout'),
    path('drf/', drf, name='drf'),
]
