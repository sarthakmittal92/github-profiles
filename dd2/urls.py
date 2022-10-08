from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
import dd2.settings

urlpatterns = [
    path('admin/', admin.site.urls) ,
    path('', include('dd2app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
# + static(dd2.settings.STATIC_URL, document_root=dd2.settings.STATIC_ROOT)