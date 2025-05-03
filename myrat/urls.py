from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from accounts.views import UserViewSet
from tasks.views import TaskViewSet


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename="users")
router.register('tasks', TaskViewSet, basename="tasks")

schema_view = get_schema_view(
   openapi.Info(
      title="Myrat Project API",
      default_version='v1',
      description="API documentation",
      contact=openapi.Contact(email="kadyr.gullyyew@gmail.com", url="https://kadyr.vercel.app"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
