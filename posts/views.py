from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ImageSerializer, SubPostSerializer, PostSerializer
from authentication.permissions import IsUserPermission
from .models import Images, Post, SubPost


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            note = serializer.save()
            if note:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class ImageListCreateView(ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.kwargs.get('note_id', None)
        return Images.objects.filter(sub_post__id=id)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('note_id', None)
        try:
            note = SubPost.objects.get(id=id)
            if note:
                serializer = ImageSerializer(
                    data=request.data, context={"request": request, "note": note})
                if serializer.is_valid():
                    data = serializer.save()
                    if data:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Team Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        return Images.objects.filter(pk=id)

    def patch(self, request, *args, **kwargs):
        image = request.data.get('note_image')
        if image is not None:
            id = self.kwargs.get('pk', None)
            note_image = Images.objects.get(id=id)
            if note_image:
                note_image.delete_image()
        return super().patch(request, *args, **kwargs)
