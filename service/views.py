from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import status, filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from service.utils import scrape_page_metadata
from .serializers import CountdownSerializer, TeamSerializer, TeamMemberSerializer, LinkViewSerializer, ProjectSerializer
from authentication.permissions import IsUserPermission, UserPermission
from .models import Countdown, Team, TeamMember, ProjectShowcase


class TeamListView(ListAPIView):
    serializer_class = TeamSerializer
    search_fields = ['team_name', 'slug']
    filterset_fields = ["status"]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    permission_classes = [IsUserPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        id = self.request.user.id
        return Team.objects.filter(owner=id)


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
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        return Team.objects.filter(slug=slug)


class TeamMemberListCreateView(ListCreateAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsUserPermission]
    search_fields = ["member_name", "position"]
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        team = get_object_or_404(Team, slug=slug)
        if team:
            return TeamMember.objects.filter(team__slug=slug)

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        try:
            team = Team.objects.get(slug=slug)
            if team:
                serializer = TeamMemberSerializer(
                    data=request.data, context={"request": request, "team": team})
                if serializer.is_valid():
                    data = serializer.save()
                    if data:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Team Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        return TeamMember.objects.filter(pk=id)

    def patch(self, request, *args, **kwargs):
        avatar = request.data.get('avatar')
        if avatar is not None:
            id = self.kwargs.get('pk', None)
            team_member = TeamMember.objects.get(id=id)
            if team_member:
                team_member.delete_avatar()
        return super().patch(request, *args, **kwargs)


class CountdownListCreateView(ListCreateAPIView):
    serializer_class = CountdownSerializer
    permission_classes = [IsUserPermission]
    search_fields = ["countdown_name", "slug"]
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


class LinkView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        URL = request.GET.get('url')
        if URL:
            validate = URLValidator()
            try:
                validate(URL)
                metadata = scrape_page_metadata(URL)
                serializer = LinkViewSerializer(metadata)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValidationError as ex:
                return Response({"detail": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "URL not found"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectListCreateView(ListCreateAPIView):
    permission_classes = [UserPermission]
    search_fields = ["project_name", "slug"]
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination
    queryset = ProjectShowcase.objects.all()


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [UserPermission]
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self):
        return ProjectShowcase.objects.all()
