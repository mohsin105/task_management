from django.urls import path
from tasks.views import dashboard,user_dashboard,manager_dashboard,create_task,show_task,update_task,delete_task
urlpatterns = [
    path('dashboard/',dashboard),
    path('user-dashboard/',user_dashboard),
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('create-task/',create_task,name='create-task'),
    path('view-task/',show_task),
    path('update-task/<int:id>/',update_task,name='update-task'),
    path('delete-task/<int:id>',delete_task,name='delete-task')
]