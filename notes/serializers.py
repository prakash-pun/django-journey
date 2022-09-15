from django.conf import settings
from rest_framework import serializers
from .models import Images, Notes


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

    def create(self, validated_data):
        note = self.context['note']
        validated_data['notes'] = note
        return super().create(validated_data)


class NoteSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()
    note_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['owner'] = owner
        return super().create(validated_data)

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))
