from django.urls import path
from .views import CustomUserView, PasswordChangeView, TokenObtainView, RefreshAccessTokenView, TokenBlacklistView, AvatarView, UserView

urlpatterns = [
    path('token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'),
    path('user/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('admin/', CustomUserView.as_view(), name='admin'),
    path('user/', UserView.as_view(), name='user'),
    path('avatar/', AvatarView.as_view(), name="user_avatar"),
    path('change-password/', PasswordChangeView.as_view(), name='change_password')
]
