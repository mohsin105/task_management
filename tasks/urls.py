from django.urls import path
from tasks.views import dashboard,CreateTask,ViewTask,TaskDetail,UpdateTask,Employee_Dashboard,Delete_Task,ManagerDashboard, CreateProject, ProjectList
urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    # path('user-dashboard/',employee_dashboard,name='user-dashboard'),
    path('user-dashboard/',Employee_Dashboard.as_view(),name='user-dashboard'),
    # path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('manager-dashboard/',ManagerDashboard.as_view(),name='manager-dashboard'),
    # path('create-task/',create_task,name='create-task'),
    path('create-task/',CreateTask.as_view(),name='create-task'),
    # path('view-task/',show_task),
    path('',ViewTask.as_view(), name='view-task'),
    # path('task/<int:task_id>/details/',task_details,name='task-details'),
    path('task/<int:task_id>/details/',TaskDetail.as_view(),name='task-details'),
    # path('update-task/<int:id>/',update_task,name='update-task'),
    path('update-task/<int:id>/',UpdateTask.as_view(),name='update-task'),
    # path('delete-task/<int:id>',delete_task,name='delete-task')
    path('delete-task/<int:id>',Delete_Task.as_view(),name='delete-task'),
    path('create-project/', CreateProject.as_view(), name='create-project'),
    path('project-list/',ProjectList.as_view(), name='project-list' )
]