
from django.urls import path, include

from app_organization.mod_project_roadmap import views_project_roadmap


urlpatterns = [
    # app_organization/project_roadmaps: DB/Model: ProjectRoadmap
    path('list_project_roadmaps/<int:pro_id>/', views_project_roadmap.list_project_roadmaps, name='list_project_roadmaps'),
    path('list_deleted_project_roadmaps/<int:pro_id>/', views_project_roadmap.list_deleted_project_roadmaps, name='list_deleted_project_roadmaps'),
    path('create_project_roadmap/<int:pro_id>/', views_project_roadmap.create_project_roadmap, name='create_project_roadmap'),
    path('edit_project_roadmap/<int:pro_id>/<int:project_roadmap_id>/', views_project_roadmap.edit_project_roadmap, name='edit_project_roadmap'),
    path('delete_project_roadmap/<int:pro_id>/<int:project_roadmap_id>/', views_project_roadmap.delete_project_roadmap, name='delete_project_roadmap'),
    path('permanent_deletion_project_roadmap/<int:pro_id>/<int:project_roadmap_id>/', views_project_roadmap.permanent_deletion_project_roadmap, name='permanent_deletion_project_roadmap'),
    path('restore_project_roadmap/<int:pro_id>/<int:project_roadmap_id>/', views_project_roadmap.restore_project_roadmap, name='restore_project_roadmap'),
    path('view_project_roadmap/<int:pro_id>/<int:project_roadmap_id>/', views_project_roadmap.view_project_roadmap, name='view_project_roadmap'),
]
