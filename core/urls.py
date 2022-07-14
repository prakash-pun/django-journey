import os
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static, serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mero Backend API",
        default_version='v1',
        description="Mero Backend API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/auth/', include("authentication.urls")),
    path('api/v1/service/', include("service.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENVIRONMENT == "DEVELOPMENT":
    from django.contrib import admin
    urlpatterns += [
        path("admin/", admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),
        path("api-auth/", include("rest_framework.urls")),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

# # Serve the favicon - Keep for later
# urlpatterns += [
#     path('favicon.ico', serve, {
#             'path': 'favicon.ico',
#             'document_root': os.path.join(BASE_DIR, 'home/static'),
#         }
#     ),
# ]
