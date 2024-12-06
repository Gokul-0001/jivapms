
from django.urls import path, include

from app_organization.mod_step import views_step


urlpatterns = [
    # app_organization/steps: DB/Model: Step
    path('list_steps/<int:activity_id>/', views_step.list_steps, name='list_steps'),
    path('list_deleted_steps/<int:activity_id>/', views_step.list_deleted_steps, name='list_deleted_steps'),
    path('create_step/<int:activity_id>/', views_step.create_step, name='create_step'),
    path('edit_step/<int:activity_id>/<int:step_id>/', views_step.edit_step, name='edit_step'),
    path('delete_step/<int:activity_id>/<int:step_id>/', views_step.delete_step, name='delete_step'),
    path('permanent_deletion_step/<int:activity_id>/<int:step_id>/', views_step.permanent_deletion_step, name='permanent_deletion_step'),
    path('restore_step/<int:activity_id>/<int:step_id>/', views_step.restore_step, name='restore_step'),
    path('view_step/<int:activity_id>/<int:step_id>/', views_step.view_step, name='view_step'),
]
