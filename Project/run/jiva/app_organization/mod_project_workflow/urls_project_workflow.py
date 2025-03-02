
from django.urls import path, include

from app_organization.mod_project_workflow import views_project_workflow


urlpatterns = [
    # app_organization/project_workflows: DB/Model: ProjectWorkflow
    path('list_project_workflows/<int:project_id>/', views_project_workflow.list_project_workflows, name='list_project_workflows'),
    path('list_deleted_project_workflows/<int:project_id>/', views_project_workflow.list_deleted_project_workflows, name='list_deleted_project_workflows'),
    path('create_project_workflow/<int:project_id>/', views_project_workflow.create_project_workflow, name='create_project_workflow'),
    path('edit_project_workflow/<int:project_id>/<int:project_workflow_id>/', views_project_workflow.edit_project_workflow, name='edit_project_workflow'),
    path('delete_project_workflow/<int:project_id>/<int:project_workflow_id>/', views_project_workflow.delete_project_workflow, name='delete_project_workflow'),
    path('permanent_deletion_project_workflow/<int:project_id>/<int:project_workflow_id>/', views_project_workflow.permanent_deletion_project_workflow, name='permanent_deletion_project_workflow'),
    path('restore_project_workflow/<int:project_id>/<int:project_workflow_id>/', views_project_workflow.restore_project_workflow, name='restore_project_workflow'),
    path('view_project_workflow/<int:project_id>/<int:project_workflow_id>/', views_project_workflow.view_project_workflow, name='view_project_workflow'),
]
