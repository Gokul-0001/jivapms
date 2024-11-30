
from django.urls import path, include

from app_organization.mod_iteration_backlog import views_iteration_backlog


urlpatterns = [
    # app_organization/iteration_backlogs: DB/Model: IterationBacklog
    path('list_iteration_backlogs/<int:iteration_id>/', views_iteration_backlog.list_iteration_backlogs, name='list_iteration_backlogs'),
    path('list_deleted_iteration_backlogs/<int:iteration_id>/', views_iteration_backlog.list_deleted_iteration_backlogs, name='list_deleted_iteration_backlogs'),
    path('create_iteration_backlog/<int:iteration_id>/', views_iteration_backlog.create_iteration_backlog, name='create_iteration_backlog'),
    path('edit_iteration_backlog/<int:iteration_id>/<int:iteration_backlog_id>/', views_iteration_backlog.edit_iteration_backlog, name='edit_iteration_backlog'),
    path('delete_iteration_backlog/<int:iteration_id>/<int:iteration_backlog_id>/', views_iteration_backlog.delete_iteration_backlog, name='delete_iteration_backlog'),
    path('permanent_deletion_iteration_backlog/<int:iteration_id>/<int:iteration_backlog_id>/', views_iteration_backlog.permanent_deletion_iteration_backlog, name='permanent_deletion_iteration_backlog'),
    path('restore_iteration_backlog/<int:iteration_id>/<int:iteration_backlog_id>/', views_iteration_backlog.restore_iteration_backlog, name='restore_iteration_backlog'),
    path('view_iteration_backlog/<int:iteration_id>/<int:iteration_backlog_id>/', views_iteration_backlog.view_iteration_backlog, name='view_iteration_backlog'),
]
