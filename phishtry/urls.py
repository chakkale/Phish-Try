from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('accounts/', include('accounts.urls')),
    path('main/', include('campaigns.urls')),
    path('', views.homepage, name="home"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
