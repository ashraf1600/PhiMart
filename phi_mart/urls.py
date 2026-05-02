from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import api_root_view

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', api_root_view),
    path('api-auth/', include('rest_framework.urls')),  # DRF auth
    path('api/v1/',include('api.urls') , name='api-root')
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
