from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from decouple import config
from django.conf import settings


LOCAL = settings.LOCAL


if LOCAL:
   schema_view = get_schema_view(
      openapi.Info(
         title="9app",
         default_version='v1',
         description="Crypto app",
         terms_of_service="https://www.google.com/policies/terms/",
         contact=openapi.Contact(email="contact@snippets.local"),
         license=openapi.License(name="BSD License"),
      ),
      public=True,
      permission_classes=(permissions.AllowAny,),
   )
else:
   schema_view = get_schema_view(
      openapi.Info(
         title="9app",
         default_version='v1',
         description="Crypto app",
         terms_of_service="https://www.google.com/policies/terms/",
         contact=openapi.Contact(email="contact@snippets.local"),
         license=openapi.License(name="BSD License"),
      ),
      public=True,
      permission_classes=(permissions.AllowAny,),
      url="https://api.9app.co",
   )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('account.urls')),
    path('user/profile/', include('userprofile.urls')),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('deposits/', include('deposit.urls')),
    path('withdrawals/', include('withdrawal.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('tradings/', include('trading.urls')),
    path('transactions/', include('transaction.urls')),
    path('wallet/', include('wallet.urls')),
    path('bank-information/', include('bank.urls')),
    path('exec/', include('exec.urls')),
    path('chat/', include('chat.urls')),
    path('broadcast/', include('broadcast.urls'))
    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('', SpectacularSwaggerView.as_view(url_name="schema")),
] 

# Add URL pattern for serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add URL pattern for serving static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
