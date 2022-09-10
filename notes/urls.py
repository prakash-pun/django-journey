from django.urls import path
from .views import NoteListCreateView, NoteDetailView

urlpatterns = [
    path('new/', NoteListCreateView.as_view(), name="create_note"),
    path('note/<int:pk>/', NoteDetailView.as_view(), name="note_detail"),
]
