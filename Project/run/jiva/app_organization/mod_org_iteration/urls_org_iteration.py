
from django.urls import path, include

from app_organization.mod_org_iteration import views_org_iteration


urlpatterns = [
    # app_organization/org_iterations: DB/Model: OrgIteration
    path('list_org_iterations/<int:org_id>/', views_org_iteration.list_org_iterations, name='list_org_iterations'),
    path('list_deleted_org_iterations/<int:org_id>/', views_org_iteration.list_deleted_org_iterations, name='list_deleted_org_iterations'),
    path('create_org_iteration/<int:org_id>/', views_org_iteration.create_org_iteration, name='create_org_iteration'),
    path('edit_org_iteration/<int:org_id>/<int:org_iteration_id>/', views_org_iteration.edit_org_iteration, name='edit_org_iteration'),
    path('delete_org_iteration/<int:org_id>/<int:org_iteration_id>/', views_org_iteration.delete_org_iteration, name='delete_org_iteration'),
    path('permanent_deletion_org_iteration/<int:org_id>/<int:org_iteration_id>/', views_org_iteration.permanent_deletion_org_iteration, name='permanent_deletion_org_iteration'),
    path('restore_org_iteration/<int:org_id>/<int:org_iteration_id>/', views_org_iteration.restore_org_iteration, name='restore_org_iteration'),
    path('view_org_iteration/<int:org_id>/<int:org_iteration_id>/', views_org_iteration.view_org_iteration, name='view_org_iteration'),
]
