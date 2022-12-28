from django.conf import settings
from rest_framework import serializers
from .models import Images, Post, Folder


class FolderSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        if 'parent_folder' in self.context:
            parent_folder = self.context['parent_folder']
            if parent_folder:
                validated_data['parent'] = parent_folder
        owner = request.user
        validated_data['created_by'] = owner
        return super().create(validated_data)

    def get_children(self, instance):
        serializer = self.__class__(instance.parent_folder.all(), many=True)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        if 'parent_post' in self.context:
            parent_post = self.context['parent_post']
            if parent_post:
                validated_data['parent'] = parent_post
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
        post = self.context['post']
        validated_data['post'] = post
        return super().create(validated_data)
