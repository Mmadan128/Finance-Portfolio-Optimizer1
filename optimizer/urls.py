# optimizer/urls.py
from django.urls import path
from .views import home, dashboard_view, optimization, portfolio, reports, login_view,register_view

urlpatterns = [
    path('', home, name='home'), # Default route
    path('login/', login_view, name='login'),  # Add login route
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('optimization/', optimization, name='optimize_portfolio'),

    path('portfolio/', portfolio, name='portfolio'),
    path('reports/', reports, name='reports'),
    path('home/', home, name='home'),
]

    

