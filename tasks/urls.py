from django.urls import path
from tasks.views import dashboard,employee_dashboard,manager_dashboard,create_task,show_task,update_task,delete_task,task_details,CreateTask,ViewTask,TaskDetail,UpdateTask
urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('user-dashboard/',employee_dashboard,name='user-dashboard'),
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    # path('create-task/',create_task,name='create-task'),
    path('create-task/',CreateTask.as_view(),name='create-task'),
    # path('view-task/',show_task),
    path('view-task/',ViewTask.as_view()),
    # path('task/<int:task_id>/details/',task_details,name='task-details'),
    path('task/<int:task_id>/details/',TaskDetail.as_view(),name='task-details'),
    # path('update-task/<int:id>/',update_task,name='update-task'),
    path('update-task/<int:id>/',UpdateTask.as_view(),name='update-task'),
    path('delete-task/<int:id>',delete_task,name='delete-task')
]