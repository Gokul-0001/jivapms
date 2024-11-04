
from django.urls import path, include

from app_organization.mod_project_template import views_project_template


urlpatterns = [
    # app_organization/project_templates: DB/Model: ProjectTemplate
    path('list_project_templates/<int:org_id>/', views_project_template.list_project_templates, name='list_project_templates'),
    path('list_deleted_project_templates/<int:org_id>/', views_project_template.list_deleted_project_templates, name='list_deleted_project_templates'),
    path('create_project_template/<int:org_id>/', views_project_template.create_project_template, name='create_project_template'),
    path('edit_project_template/<int:org_id>/<int:project_template_id>/', views_project_template.edit_project_template, name='edit_project_template'),
    path('delete_project_template/<int:org_id>/<int:project_template_id>/', views_project_template.delete_project_template, name='delete_project_template'),
    path('permanent_deletion_project_template/<int:org_id>/<int:project_template_id>/', views_project_template.permanent_deletion_project_template, name='permanent_deletion_project_template'),
    path('restore_project_template/<int:org_id>/<int:project_template_id>/', views_project_template.restore_project_template, name='restore_project_template'),
    path('view_project_template/<int:org_id>/<int:project_template_id>/', views_project_template.view_project_template, name='view_project_template'),
]
