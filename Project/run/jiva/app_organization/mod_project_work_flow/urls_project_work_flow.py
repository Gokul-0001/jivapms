
from django.urls import path, include

from app_organization.mod_project_work_flow import views_project_work_flow


urlpatterns = [
    # app_organization/project_work_flows: DB/Model: ProjectWorkFlow
    path('list_project_work_flows/<int:pro_id>/', views_project_work_flow.list_project_work_flows, name='list_project_work_flows'),
    path('list_deleted_project_work_flows/<int:pro_id>/', views_project_work_flow.list_deleted_project_work_flows, name='list_deleted_project_work_flows'),
    path('create_project_work_flow/<int:pro_id>/', views_project_work_flow.create_project_work_flow, name='create_project_work_flow'),
    path('edit_project_work_flow/<int:pro_id>/<int:project_work_flow_id>/', views_project_work_flow.edit_project_work_flow, name='edit_project_work_flow'),
    path('delete_project_work_flow/<int:pro_id>/<int:project_work_flow_id>/', views_project_work_flow.delete_project_work_flow, name='delete_project_work_flow'),
    path('permanent_deletion_project_work_flow/<int:pro_id>/<int:project_work_flow_id>/', views_project_work_flow.permanent_deletion_project_work_flow, name='permanent_deletion_project_work_flow'),
    path('restore_project_work_flow/<int:pro_id>/<int:project_work_flow_id>/', views_project_work_flow.restore_project_work_flow, name='restore_project_work_flow'),
    path('view_project_work_flow/<int:pro_id>/<int:project_work_flow_id>/', views_project_work_flow.view_project_work_flow, name='view_project_work_flow'),
]
