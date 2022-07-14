from rest_framework import serializers
from core import settings
from service.models import Team, TeamMember


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




