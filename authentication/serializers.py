from core import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import CustomUser, User


class MyTokenObtaionPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtaionPairSerializer, cls).get_token(user)

        token['user_id'] = user.id
        token['user_type'] = user.user_type
        token['username'] = user.username

        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    class Meta:
        extra_kwargs = {'refresh': {'required': False}}

    def validate(self, attrs):
        refresh_cookie = self.context.get(
            'request').COOKIES.get('refresh_token')
        refresh_token = refresh_cookie
        if refresh_token is None:
            raise serializers.ValidationError(
                {"refresh": "This field is required."})

        attrs['refresh'] = refresh_token
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email',
                    'password', 'user_type', 'avatar', 'is_active', 'email_verified', 'last_login']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {
            'write_only': True}, 'email_verified': {'read_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), ])
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password', 'user_type', 'avatar', 'bio', 'location', 'website', 'github_username', 'is_active', 'linkedln_username','email_verified', 'created_at', "updated_at"]
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {
            'write_only': True}, 'email_verified': {'read_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))


    def update(self, instance, validated_data):
        if('password' in [x for x in validated_data]):
            validated_data.pop('password')
        return super().update(instance, validated_data)


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ("avatar", )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, value):
        new_password = value.get('new_password', '')
        confirm_new_password = value.get('confirm_new_password', '')
        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {"detail": "New Password Didn't match"})
        return value


class ConfirmPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    class Meta:
        fields = ["password"]

    def validate(self, value):
        password = value.get('password', '')
        request = self.context.get('request')
        user= request.user
        if not password:
            raise serializers.ValidationError({"detail": "Password Not Found"})
        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Password didn't match"})
        return value