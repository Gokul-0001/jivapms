
from django.urls import path, include

from app_organization.mod_organizationdetail import views_organizationdetail


urlpatterns = [
    # app_organization/organizationdetails: DB/Model: Organizationdetail
    path('list_organizationdetails/<int:org_id>/', views_organizationdetail.list_organizationdetails, name='list_organizationdetails'),
    path('list_deleted_organizationdetails/<int:org_id>/', views_organizationdetail.list_deleted_organizationdetails, name='list_deleted_organizationdetails'),
    path('create_organizationdetail/<int:org_id>/', views_organizationdetail.create_organizationdetail, name='create_organizationdetail'),
    path('edit_organizationdetail/<int:org_id>/<int:organizationdetail_id>/', views_organizationdetail.edit_organizationdetail, name='edit_organizationdetail'),
    path('delete_organizationdetail/<int:org_id>/<int:organizationdetail_id>/', views_organizationdetail.delete_organizationdetail, name='delete_organizationdetail'),
    path('permanent_deletion_organizationdetail/<int:org_id>/<int:organizationdetail_id>/', views_organizationdetail.permanent_deletion_organizationdetail, name='permanent_deletion_organizationdetail'),
    path('restore_organizationdetail/<int:org_id>/<int:organizationdetail_id>/', views_organizationdetail.restore_organizationdetail, name='restore_organizationdetail'),
    path('view_organizationdetail/<int:org_id>/<int:organizationdetail_id>/', views_organizationdetail.view_organizationdetail, name='view_organizationdetail'),
]
