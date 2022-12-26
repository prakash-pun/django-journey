from django.conf import settings
from rest_framework import serializers
from .models import Images, SubPost, Post


class PostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField()

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
        note = self.context['note']
        validated_data['subposts'] = note
        return super().create(validated_data)


class SubPostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()
    note_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = SubPost
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['owner'] = owner
        return super().create(validated_data)

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))
