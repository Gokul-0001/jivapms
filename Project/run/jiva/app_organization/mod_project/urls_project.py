
from django.urls import path, include

from app_organization.mod_project import views_project, views_project_roadmap


urlpatterns = [
    # app_organization/projects: DB/Model: Project
    path('project_homepage/<int:org_id>/<int:project_id>/', views_project.project_homepage, name='project_homepage'),
    path('list_projects/<int:org_id>/', views_project.list_projects, name='list_projects'),
    path('list_deleted_projects/<int:org_id>/', views_project.list_deleted_projects, name='list_deleted_projects'),
    path('create_project/<int:org_id>/', views_project.create_project, name='create_project'),
    path('edit_project/<int:org_id>/<int:project_id>/', views_project.edit_project, name='edit_project'),
    path('delete_project/<int:org_id>/<int:project_id>/', views_project.delete_project, name='delete_project'),
    path('permanent_deletion_project/<int:org_id>/<int:project_id>/', views_project.permanent_deletion_project, name='permanent_deletion_project'),
    path('restore_project/<int:org_id>/<int:project_id>/', views_project.restore_project, name='restore_project'),
    path('view_project/<int:org_id>/<int:project_id>/', views_project.view_project, name='view_project'),
    path('project_settings_page/<int:org_id>/<int:project_id>/', views_project.project_settings_page, name='project_settings_page'),
    path('project_dvs/<int:org_id>/<int:project_id>/', views_project.project_dvs, name='project_dvs'),
    
    path('project_roadmap/<int:org_id>/<int:project_id>/', views_project_roadmap.project_roadmap, name='project_roadmap'),
    path('ajax_update_project_roadmap/', views_project_roadmap.ajax_update_project_roadmap, name='ajax_update_project_roadmap'),
    
    
]
