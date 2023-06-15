from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from products.views import RegisterView, LoginView, logout_view, ProfileView
from .yasg import urlpatterns as docs_url

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('products/', include('products.urls')),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('api/', include('products.api.urls')),
]

urlpatterns += docs_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
