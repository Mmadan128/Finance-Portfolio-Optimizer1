# portfolio_optimizer/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication routes
    path('', include('optimizer.urls')),  # App-specific routes
]
