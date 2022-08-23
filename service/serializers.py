from django.utils import timezone
from rest_framework import serializers
from core import settings
from service.models import Team, TeamMember, Countdown


class TeamMemberSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField()

    class Meta:
        model = TeamMember
        fields = '__all__'

    def create(self, validated_data):
        team = self.context['team']
        validated_data['team'] = team
        return super().create(validated_data)


class TeamSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    owner_name = serializers.ReadOnlyField()
    team_members = TeamMemberSerializer(many=True, read_only=True, source='team_member')

    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {'slug': {'read_only': True}}

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['owner'] = owner
        return super().create(validated_data)

    def get_avatar(self, instance):
        image = instance.avatar
        return self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(image))


class CountdownSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField()

    class Meta:
        model = Countdown
        fields = '__all__'
        extra_kwargs = {'slug': {'read_only': True}}

    def validate_date_time(self, data):
        if data < timezone.now():
            raise serializers.ValidationError("Date must be greater than current date time.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        owner = request.user
        validated_data['owner'] = owner
        return super().create(validated_data)


class LinkViewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField()
    favicon = serializers.CharField()
    sitename = serializers.CharField()
    color = serializers.CharField()
    url = serializers.CharField()
