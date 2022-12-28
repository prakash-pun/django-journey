from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import FolderSerializer, ImageSerializer, PostSerializer
from authentication.permissions import IsUserPermission
from .models import Folder, Images, Post


class FolderListCreateView(ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Folder.objects.filter(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        parent_id = request.POST.get('parent_id')
        context = {'request': request}
        # context['request'] = request
        if parent_id:
            parent_folder = get_object_or_404(Folder, id=parent_id)
            if parent_folder is not None:
                context['parent_folder'] = parent_folder
                serializer = FolderSerializer(
                    data=request.data, context=context)
                if serializer.is_valid():
                    data = serializer.save()
                    if data:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Folder not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FolderSerializer(
                data=request.data, context=context)
            if serializer.is_valid():
                data = serializer.save()
                if data:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsUserPermission]
    lookup_field = "slug"

    def get_queryset(self):
        return Folder.objects.filter(created_by=self.request.user)


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        post_parent_id = request.POST.get('post_parent_id')
        context = {'request': request}
        if post_parent_id:
            parent_post = get_object_or_404(Post, id=post_parent_id)
            if parent_post is not None:
                context['parent_post'] = parent_post
                serializer = PostSerializer(data=request.data, context=context)
                if serializer.is_valid():
                    data = serializer.save()
                    if data:
                        return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Post not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = PostSerializer(
                data=request.data, context=context)
            if serializer.is_valid():
                note = serializer.save()
                if note:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)


class ImageListCreateView(ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        return Images.objects.filter(sub_post__id=id)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk', None)
        try:
            post = Post.objects.get(id=id)
            if post:
                serializer = ImageSerializer(
                    data=request.data, context={"request": request, "post": post})
                if serializer.is_valid():
                    data = serializer.save()
                    if data:
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsUserPermission]

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        return Images.objects.filter(pk=id)

    def patch(self, request, *args, **kwargs):
        image = request.data.get('post_image')
        if image is not None:
            id = self.kwargs.get('pk', None)
            post_image = Images.objects.get(id=id)
            if post_image:
                post_image.delete_image()
        return super().patch(request, *args, **kwargs)
