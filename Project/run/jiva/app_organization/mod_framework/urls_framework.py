
from django.urls import path, include

from app_organization.mod_framework import views_framework


urlpatterns = [
    # app_organization/frameworks: DB/Model: Framework
    path('list_frameworks/<int:organization_id>/', views_framework.list_frameworks, name='list_frameworks'),
    path('list_deleted_frameworks/<int:organization_id>/', views_framework.list_deleted_frameworks, name='list_deleted_frameworks'),
    path('create_framework/<int:organization_id>/', views_framework.create_framework, name='create_framework'),
    path('edit_framework/<int:organization_id>/<int:framework_id>/', views_framework.edit_framework, name='edit_framework'),
    path('delete_framework/<int:organization_id>/<int:framework_id>/', views_framework.delete_framework, name='delete_framework'),
    path('permanent_deletion_framework/<int:organization_id>/<int:framework_id>/', views_framework.permanent_deletion_framework, name='permanent_deletion_framework'),
    path('restore_framework/<int:organization_id>/<int:framework_id>/', views_framework.restore_framework, name='restore_framework'),
    path('view_framework/<int:organization_id>/<int:framework_id>/', views_framework.view_framework, name='view_framework'),
]
