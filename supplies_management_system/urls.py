# supplies_management_system_test/urls.py (or your main urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static
from django.views.generic.base import RedirectView # Import RedirectView
from django.urls import reverse_lazy # Import reverse_lazy

# Import login/logout views from supply app (or move them to a core app)
from supply.views import login_page, logout_page, index

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include django-select2 URLs
    path('select2/', include('django_select2.urls')),
    
    # Authentication (using views from supply app for now)
    # path('', login_page, name='login'), # Root redirects to login
    # path('login/', login_page, name='login'), # Explicit login path
    path('', RedirectView.as_view(url=reverse_lazy('customer:login'), permanent=False), name='root_redirect'),
    path('manager/login/', login_page, name='manager_login'), # Explicit login path for managers/staff (was 'login')
    path('logout/', logout_page, name='logout'),

    # Include supply app URLs (for manager actions, items, suppliers etc.)
    path('supply/', include('supply.urls', namespace='supply')),

    # Include customer app URLs
    path('customer/', include('customer.urls', namespace='customer')),
]

# Add media file serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

