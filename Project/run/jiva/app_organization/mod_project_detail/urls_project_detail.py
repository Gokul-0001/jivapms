
from django.urls import path, include

from app_organization.mod_project_detail import views_project_detail


urlpatterns = [
    # app_organization/project_details: DB/Model: ProjectDetail
    path('list_project_details/<int:pro_id>/', views_project_detail.list_project_details, name='list_project_details'),
    path('list_deleted_project_details/<int:pro_id>/', views_project_detail.list_deleted_project_details, name='list_deleted_project_details'),
    path('create_project_detail/<int:pro_id>/', views_project_detail.create_project_detail, name='create_project_detail'),
    path('edit_project_detail/<int:pro_id>/<int:project_detail_id>/', views_project_detail.edit_project_detail, name='edit_project_detail'),
    path('delete_project_detail/<int:pro_id>/<int:project_detail_id>/', views_project_detail.delete_project_detail, name='delete_project_detail'),
    path('permanent_deletion_project_detail/<int:pro_id>/<int:project_detail_id>/', views_project_detail.permanent_deletion_project_detail, name='permanent_deletion_project_detail'),
    path('restore_project_detail/<int:pro_id>/<int:project_detail_id>/', views_project_detail.restore_project_detail, name='restore_project_detail'),
    path('view_project_detail/<int:pro_id>/<int:project_detail_id>/', views_project_detail.view_project_detail, name='view_project_detail'),
]
