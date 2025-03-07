
from django.urls import path, include

from app_organization.mod_productx import views_productx


urlpatterns = [
    # app_organization/productxes: DB/Model: Productx
    path('list_productxes/<int:organization_id>/', views_productx.list_productxes, name='list_productxes'),
    path('list_deleted_productxes/<int:organization_id>/', views_productx.list_deleted_productxes, name='list_deleted_productxes'),
    path('create_productx/<int:organization_id>/', views_productx.create_productx, name='create_productx'),
    path('edit_productx/<int:organization_id>/<int:productx_id>/', views_productx.edit_productx, name='edit_productx'),
    path('delete_productx/<int:organization_id>/<int:productx_id>/', views_productx.delete_productx, name='delete_productx'),
    path('permanent_deletion_productx/<int:organization_id>/<int:productx_id>/', views_productx.permanent_deletion_productx, name='permanent_deletion_productx'),
    path('restore_productx/<int:organization_id>/<int:productx_id>/', views_productx.restore_productx, name='restore_productx'),
    path('view_productx/<int:organization_id>/<int:productx_id>/', views_productx.view_productx, name='view_productx'),
]
