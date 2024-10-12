
from django.urls import path, include

from app_memberprofilerole.mod_memberorganizationrole import views_memberorganizationrole


urlpatterns = [
    # app_memberprofilerole/memberorganizationroles: DB/Model: Memberorganizationrole
    path('list_memberorganizationroles/<int:org_id>/', views_memberorganizationrole.list_memberorganizationroles, name='list_memberorganizationroles'),
    path('list_deleted_memberorganizationroles/<int:org_id>/', views_memberorganizationrole.list_deleted_memberorganizationroles, name='list_deleted_memberorganizationroles'),
    path('create_memberorganizationrole/<int:org_id>/', views_memberorganizationrole.create_memberorganizationrole, name='create_memberorganizationrole'),
    path('edit_memberorganizationrole/<int:org_id>/<int:memberorganizationrole_id>/', views_memberorganizationrole.edit_memberorganizationrole, name='edit_memberorganizationrole'),
    path('delete_memberorganizationrole/<int:org_id>/<int:memberorganizationrole_id>/', views_memberorganizationrole.delete_memberorganizationrole, name='delete_memberorganizationrole'),
    path('permanent_deletion_memberorganizationrole/<int:org_id>/<int:memberorganizationrole_id>/', views_memberorganizationrole.permanent_deletion_memberorganizationrole, name='permanent_deletion_memberorganizationrole'),
    path('restore_memberorganizationrole/<int:org_id>/<int:memberorganizationrole_id>/', views_memberorganizationrole.restore_memberorganizationrole, name='restore_memberorganizationrole'),
    path('view_memberorganizationrole/<int:org_id>/<int:memberorganizationrole_id>/', views_memberorganizationrole.view_memberorganizationrole, name='view_memberorganizationrole'),
]
