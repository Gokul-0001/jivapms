
from django.urls import path, include

from app_organization.mod_org_work_flow import views_org_work_flow


urlpatterns = [
    # app_organization/org_work_flows: DB/Model: OrgWorkFlow
    path('list_org_work_flows/<int:org_id>/', views_org_work_flow.list_org_work_flows, name='list_org_work_flows'),
    path('list_deleted_org_work_flows/<int:org_id>/', views_org_work_flow.list_deleted_org_work_flows, name='list_deleted_org_work_flows'),
    path('create_org_work_flow/<int:org_id>/', views_org_work_flow.create_org_work_flow, name='create_org_work_flow'),
    path('edit_org_work_flow/<int:org_id>/<int:org_work_flow_id>/', views_org_work_flow.edit_org_work_flow, name='edit_org_work_flow'),
    path('delete_org_work_flow/<int:org_id>/<int:org_work_flow_id>/', views_org_work_flow.delete_org_work_flow, name='delete_org_work_flow'),
    path('permanent_deletion_org_work_flow/<int:org_id>/<int:org_work_flow_id>/', views_org_work_flow.permanent_deletion_org_work_flow, name='permanent_deletion_org_work_flow'),
    path('restore_org_work_flow/<int:org_id>/<int:org_work_flow_id>/', views_org_work_flow.restore_org_work_flow, name='restore_org_work_flow'),
    path('view_org_work_flow/<int:org_id>/<int:org_work_flow_id>/', views_org_work_flow.view_org_work_flow, name='view_org_work_flow'),
]
