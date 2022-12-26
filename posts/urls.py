from django.urls import path
from .views import ImageDetailView, ImageListCreateView, PostListCreateView, PostDetailView, SubPostListCreateView, SubPostDetailView

urlpatterns = [
    path('post/', PostListCreateView.as_view(), name="create_post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="note_detail"),
    path('subpost/<slug:slug>/',
         SubPostListCreateView.as_view(), name='subpost_create'),
    path('subpost-detail/<int:pk>/',
         SubPostDetailView.as_view(), name='subpost_detail'),
    path('subpost/images/<int:pk>/',
         ImageListCreateView.as_view(), name="image_list_create"),
    path('subpost/image-detail/<int:pk>/',
         ImageDetailView.as_view(), name="image_detail"),
]
