from django.urls import path
from users.views import sign_up,activate_user,admin_dashboard,group_list,Greetings,HiGreetings,CustomLoginView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView,EditProfileView,AssignRole,CreateGroup,GroupList
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from tasks.views import AdminViewTask

urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    # path('sign-in/',sign_in,name='sign-in'),
    # path('sign-in/',LoginView.as_view(),name='sign-in'),
    path('sign-in/',CustomLoginView.as_view(),name='sign-in'),
    # path('logout/',sign_out,name='logout'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin/dashboard/',admin_dashboard,name='admin-dashboard'),
    # path('admin/<int:user_id>/assign-role/', assign_role,name='assign-role'),
    path('admin/<int:user_id>/assign-role/', AssignRole.as_view(),name='assign-role'),
    # path('admin/create-group',create_group,name='create-group'),
    path('admin/create-group',CreateGroup.as_view(),name='create-group'),
    # path('admin/group-list/',group_list,name='group-list'),
    path('admin/group-list/',GroupList.as_view(),name='group-list'),
    path('admin/view-task/',AdminViewTask.as_view(), name='admin-view-task'),
    path('greetings',HiGreetings.as_view(greetings='Kemon acho')),
    # path('profile',TemplateView.as_view(template_name='accounts/profile.html'),name='')
    path('profile',ProfileView.as_view(),name='profile'),
    path('edit-profile',EditProfileView.as_view(),name='edit-profile'),
    # path('password-change',PasswordChangeView.as_view(template_name='accounts/password_change.html'),name='password-change'),
    path('password-change',ChangePassword.as_view(),name='password-change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password-reset',CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm') #default name='' used, shown in docs in ccdv
]
