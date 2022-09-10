from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import NoteSerializer
from authentication.permissions import IsUserPermission
from .models import Notes


class NoteListCreateView(ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Notes.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = NoteSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            note = serializer.save()
            if note:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Notes.objects.filter(owner=self.request.user)
