from django.conf import settings
from rest_framework import serializers
from .models import Images, Post, SubPost


class PostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['created_by'] = owner
        return super().create(validated_data)

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

    def create(self, validated_data):
        subpost = self.context['subpost']
        validated_data['sub_post'] = subpost
        return super().create(validated_data)


class SubPostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()
    subpost_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubPost
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        post = self.context['post']
        owner = request.user
        validated_data['created_by'] = owner
        validated_data['post'] = post
        return super().create(validated_data)

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))
