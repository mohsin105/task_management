from django.urls import path
from tasks.views import dashboard
urlpatterns = [
    path('dashboard/',dashboard)
]