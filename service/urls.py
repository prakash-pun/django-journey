from django.urls import path
from .views import CountdownDetailView, CountdownListCreateView, LinkView, TeamCreateView, TeamListView, TeamDetailView, TeamMemberListCreateView, TeamMemberDetailView, ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('create-team/', TeamCreateView.as_view(), name='team'),
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team-detail/<slug:slug>/', TeamDetailView.as_view(), name='team_detail'),
    path('team-member/<slug:slug>/',
         TeamMemberListCreateView.as_view(), name='team_member'),
    path('team-member-detail/<int:pk>/',
         TeamMemberDetailView.as_view(), name='team_member_detail'),
    path('countdown/', CountdownListCreateView.as_view(), name='countdown'),
    path('countdown/<int:pk>/', CountdownDetailView.as_view(),
         name='countdown_detail'),
    path('link-preview/', LinkView.as_view(), name="link_preview"),
    path('project/', ProjectListCreateView.as_view(), name='project'),
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail')
]
