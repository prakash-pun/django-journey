from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import filters
from rest_framework import status
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import ChangePasswordSerializer, NewPasswordSerializer, PasswordResetSerializer, UserSerializer, MyTokenObtaionPairSerializer, CustomTokenRefreshSerializer, AvatarSerializer, CustomUserSerializer
from .permissions import IsAdminPermission, IsAdminOrUserPermission, IsUserPermission
from .models import User


class TokenObtainView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtaionPairSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        refresh_token = serializer.validated_data['refresh']
        # access_token = serializer.validated_data['access']
        get_token(request)
        res.set_cookie("refresh_token", refresh_token, max_age=settings.SIMPLE_JWT.get(
            'REFRESH_TOKEN_LIFETIME').total_seconds(), samesite='Lax', secure=False, httponly=True)
        res.data.pop('refresh')
        return res


class RefreshAccessTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        data['refresh'] = "TOKEN_IN_HTTPONLY_COOKIE"
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenBlacklistView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # refresh_token = request.data["refresh_token"]
            refresh_token = request.COOKIES.get(
                settings.SIMPLE_JWT.get('REFRESH_COOKIE_NAME'))
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(
                settings.SIMPLE_JWT.get('REFRESH_COOKIE_NAME'))
            return response
        except Exception as ex:
            return Response({"detail": "error occured", "error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserView(APIView):
    permission_classes = [IsAdminPermission]

    def get(self, request):
        try:
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        avatar = request.data.get('avatar')
        if avatar is not None:
            user = request.user
            user.delete_avatar()
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format='json'):
        try:
            serializer = CustomUserSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    json = serializer.data
                    return Response(json, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            return Response({"detail": "Error creating user", "error": str(exe)}, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = PasswordResetSerializer(
#             data=request.data, context={'request': request})
#         if serializer.is_valid():
#             email = request.data["email"]
#             user = User.objects.filter(email=email).last()
#             if user:
#                 token = account_activation_token.make_token(user)
#                 absurl = CLIENT_URL + "/password/reset/" + \
#                     "token=" + str(token) + "&identifier=" + str(user.id)
#                 try:
#                     send_password_reset_email.delay('forget-password.html', CLIENT_URL, token, absurl, user.username, user.email, user.id)
#                     return Response({'detail': 'Password Reset Email Sent'}, status=status.HTTP_200_OK)
#                 except Exception:
#                     return Response({'detail': 'Error sending email'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response({'detail': 'Cannot find an email'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NewPasswordView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         token = request.GET.get('token')
#         identifier = request.GET.get('identifier')

#         try:
#             user = User.objects.get(id=identifier)
#             if user is not None:
#                 if not account_activation_token.check_token(user, token):
#                     return Response({'detail': 'Activation Link Invalid'}, status=status.HTTP_400_BAD_REQUEST)
#                 return Response({"detail": "Password Token Valid"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': 'Cannot Find User'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ex:
#             user = None
#             return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):
#         token = request.GET.get('token')
#         identifier = request.GET.get('identifier')

#         try:
#             user = User.objects.get(id=identifier)
#             if user is not None:
#                 if not account_activation_token.check_token(user, token):
#                     return Response({'detail': 'Activation Link Invalid'}, status=status.HTTP_400_BAD_REQUEST)
#                 serializer = NewPasswordSerializer(data=request.data)
#                 if serializer.is_valid():
#                     user.set_password(serializer.data.get("new_password"))
#                     user.save()
#                     return Response({'detail': "Password Changed Successfully"}, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'detail': 'Cannot Find User'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ex:
#             user = None
#             return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsUserPermission]

    def get(self, request):
        instance = User.objects.filter(pk=request.user.id).last()
        if instance is not None:
            serializer = UserSerializer(instance)
            return Response(serializer.data)
        else:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"detail": "Password didn't match"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAdminOrUserPermission]

    def get(self, request):
        try:
            user = request.user
            instance = User.objects.get(id=user.pk)
            if instance:
                serializer = UserSerializer(
                    instance, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format='json'):
        try:
            serializer = UserSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as err:
            return Response(err.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            return Response({"detail": "Error creating user", "error": str(exe)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        avatar = request.data.get('avatar')
        if avatar is not None:
            user = request.user
            user.delete_avatar()
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ListUserView(ListAPIView):
    permission_classes = [IsAdminPermission]
    pagination_class = LimitOffsetPagination
    search_fields = ["full_name", "email", "username"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AvatarView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            user = request.user
            instance = User.objects.get(id=user.id)
            if instance:
                serializer = AvatarSerializer(instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
