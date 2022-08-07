from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CountdownSerializer, TeamSerializer, TeamMemberSerializer
from authentication.permissions import IsUserPermission, UserPermission
from .models import Countdown, Team, TeamMember


class TeamListView(ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.kwargs.get('slug', None)
        return Team.objects.filter(owner__username=username)


class TeamCreateView(CreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsUserPermission]

    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            note = serializer.save()
            if note:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [UserPermission]
    lookup_field="slug"

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        return Team.objects.filter(slug=slug)


class TeamMemberListCreateView(ListCreateAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        return TeamMember.objects.filter(team__slug=slug)

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        try:
            team = Team.objects.get(slug=slug)
            if team:
                serializer = TeamMemberSerializer(
                data=request.data, context={"request": request, "team": team})
                if serializer.is_valid():
                    note = serializer.save()
                    if note:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Team Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        return TeamMember.objects.filter(team__slug=slug)


class CountdownListCreateView(ListCreateAPIView):
    serializer_class = CountdownSerializer
    permission_classes = [IsUserPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        id = self.request.user.id
        return Countdown.objects.filter(owner=id)


class CountdownDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CountdownSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.request.user.id
        return Countdown.objects.filter(owner=id)
