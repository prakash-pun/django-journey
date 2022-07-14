from django.urls import path
from .views import TeamCreateView, TeamListView, TeamDetailView, TeamMemberListCreateView, TeamMemberDetailView

urlpatterns = [
    path('create-team/', TeamCreateView.as_view(), name='team'),
    path('team/<slug:slug>/', TeamListView.as_view(), name='team_list'),
    path('team-detail/<slug:slug>/', TeamDetailView.as_view(), name='team_detail'),
    path('team-member/<slug:slug>/', TeamMemberListCreateView.as_view(), name='team_member'),
    path('team-member-detail/<slug:slug>/<int:pk>/', TeamMemberDetailView.as_view(), name='team_member_detail'),
]
