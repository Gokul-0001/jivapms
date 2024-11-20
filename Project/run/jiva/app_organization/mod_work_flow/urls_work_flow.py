
from django.urls import path, include

from app_organization.mod_work_flow import views_work_flow


urlpatterns = [
    # app_organization/work_flows: DB/Model: WorkFlow
    path('list_work_flows/<int:pro_id>/', views_work_flow.list_work_flows, name='list_work_flows'),
    path('list_deleted_work_flows/<int:pro_id>/', views_work_flow.list_deleted_work_flows, name='list_deleted_work_flows'),
    path('create_work_flow/<int:pro_id>/', views_work_flow.create_work_flow, name='create_work_flow'),
    path('edit_work_flow/<int:pro_id>/<int:work_flow_id>/', views_work_flow.edit_work_flow, name='edit_work_flow'),
    path('delete_work_flow/<int:pro_id>/<int:work_flow_id>/', views_work_flow.delete_work_flow, name='delete_work_flow'),
    path('permanent_deletion_work_flow/<int:pro_id>/<int:work_flow_id>/', views_work_flow.permanent_deletion_work_flow, name='permanent_deletion_work_flow'),
    path('restore_work_flow/<int:pro_id>/<int:work_flow_id>/', views_work_flow.restore_work_flow, name='restore_work_flow'),
    path('view_work_flow/<int:pro_id>/<int:work_flow_id>/', views_work_flow.view_work_flow, name='view_work_flow'),
]
