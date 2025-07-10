# supplies_management_system_test/urls.py (or your main urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static
from django.views.generic.base import RedirectView # Import RedirectView
from django.urls import reverse_lazy # Import reverse_lazy
from django.shortcuts import redirect # Import redirect

# Import login/logout views from supply app (or move them to a core app)
from supply.views import login_page, logout_page, index

urlpatterns = [
    path('', lambda request: redirect('manager_login'), name='root_redirect'),  # Redirect root to manager login
    path('admin/', admin.site.urls),
    # Include django-select2 URLs
    path('select2/', include('django_select2.urls')),
    path('manager/login/', login_page, name='manager_login'), # Explicit login path for managers/staff (was 'login')
    path('logout/', logout_page, name='logout'),

    # Include supply app URLs (for manager actions, items, suppliers etc.)
    path('supply/', include('supply.urls', namespace='supply')),
    
    # Include customer app URLs
    # This will handle customer registration, login, dashboard etc.
    path('customer/', include('customer.urls', namespace='customer')),
    
    # Include supplier app URLs
    # This will handle supplier registration, login, dashboard etc.
    path('supplier/', include('supplier.urls', namespace='supplier')),
    
]

# Add media file serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

