from django.urls import path
from tasks.views import dashboard,user_dashboard,manager_dashboard
urlpatterns = [
    path('dashboard/',dashboard),
    path('user-dashboard/',user_dashboard),
    path('manager-dashboard/',manager_dashboard)
]