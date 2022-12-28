from django.urls import path
from .views import FolderListCreateView, FolderDetailView, PostListCreateView, PostDetailView,  ImageDetailView, ImageListCreateView

urlpatterns = [
    path('folder/', FolderListCreateView.as_view(), name='list_create_folder'),
    path('folder/<slug:slug>/', FolderDetailView.as_view(), name='folder_detail'),
    path('post/', PostListCreateView.as_view(), name="create_post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('images/<int:pk>/', ImageListCreateView.as_view(), name="image_list"),
    path('image-detail/<int:pk>/', ImageDetailView.as_view(), name="image_detail"),
]
