from django.urls import path
from .views import TokenObtainView, RefreshAccessTokenView, TokenBlacklistView, AvatarView, UserView

urlpatterns = [
    path('token/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'),
    path('user/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('avatar/', AvatarView.as_view(), name="user_avatar"),
    path('user/', UserView.as_view(), name='user')
]
