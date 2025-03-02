
from django.urls import path, include

from app_organization.mod_project_workflow_step import views_project_workflow_step


urlpatterns = [
    # app_organization/project_workflow_steps: DB/Model: ProjectWorkflowStep
    path('list_project_workflow_steps/<int:project_workflow_id>/', views_project_workflow_step.list_project_workflow_steps, name='list_project_workflow_steps'),
    path('list_deleted_project_workflow_steps/<int:project_workflow_id>/', views_project_workflow_step.list_deleted_project_workflow_steps, name='list_deleted_project_workflow_steps'),
    path('create_project_workflow_step/<int:project_workflow_id>/', views_project_workflow_step.create_project_workflow_step, name='create_project_workflow_step'),
    path('edit_project_workflow_step/<int:project_workflow_id>/<int:project_workflow_step_id>/', views_project_workflow_step.edit_project_workflow_step, name='edit_project_workflow_step'),
    path('delete_project_workflow_step/<int:project_workflow_id>/<int:project_workflow_step_id>/', views_project_workflow_step.delete_project_workflow_step, name='delete_project_workflow_step'),
    path('permanent_deletion_project_workflow_step/<int:project_workflow_id>/<int:project_workflow_step_id>/', views_project_workflow_step.permanent_deletion_project_workflow_step, name='permanent_deletion_project_workflow_step'),
    path('restore_project_workflow_step/<int:project_workflow_id>/<int:project_workflow_step_id>/', views_project_workflow_step.restore_project_workflow_step, name='restore_project_workflow_step'),
    path('view_project_workflow_step/<int:project_workflow_id>/<int:project_workflow_step_id>/', views_project_workflow_step.view_project_workflow_step, name='view_project_workflow_step'),

    path('add_project_workflow_step/<int:project_workflow_id>/', views_project_workflow_step.add_project_workflow_step, name='add_project_workflow_step'),
]
