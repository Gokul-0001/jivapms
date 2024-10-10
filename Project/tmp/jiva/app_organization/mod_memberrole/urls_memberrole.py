
from django.urls import path, include

from app_organization.mod_memberrole import views_memberrole


urlpatterns = [
    # app_organization/memberroles: DB/Model: Memberrole
    path('list_memberroles/<int:org_id>/', views_memberrole.list_memberroles, name='list_memberroles'),
    path('list_deleted_memberroles/<int:org_id>/', views_memberrole.list_deleted_memberroles, name='list_deleted_memberroles'),
    path('create_memberrole/<int:org_id>/', views_memberrole.create_memberrole, name='create_memberrole'),
    path('edit_memberrole/<int:org_id>/<int:memberrole_id>/', views_memberrole.edit_memberrole, name='edit_memberrole'),
    path('delete_memberrole/<int:org_id>/<int:memberrole_id>/', views_memberrole.delete_memberrole, name='delete_memberrole'),
    path('permanent_deletion_memberrole/<int:org_id>/<int:memberrole_id>/', views_memberrole.permanent_deletion_memberrole, name='permanent_deletion_memberrole'),
    path('restore_memberrole/<int:org_id>/<int:memberrole_id>/', views_memberrole.restore_memberrole, name='restore_memberrole'),
    path('view_memberrole/<int:org_id>/<int:memberrole_id>/', views_memberrole.view_memberrole, name='view_memberrole'),
]
