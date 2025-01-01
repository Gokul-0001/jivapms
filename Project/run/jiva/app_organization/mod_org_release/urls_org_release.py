
from django.urls import path, include

from app_organization.mod_org_release import views_org_release


urlpatterns = [
    # app_organization/org_releases: DB/Model: OrgRelease
    path('list_org_releases/<int:org_id>/', views_org_release.list_org_releases, name='list_org_releases'),
    path('list_deleted_org_releases/<int:org_id>/', views_org_release.list_deleted_org_releases, name='list_deleted_org_releases'),
    path('create_org_release/<int:org_id>/', views_org_release.create_org_release, name='create_org_release'),
    path('edit_org_release/<int:org_id>/<int:org_release_id>/', views_org_release.edit_org_release, name='edit_org_release'),
    path('delete_org_release/<int:org_id>/<int:org_release_id>/', views_org_release.delete_org_release, name='delete_org_release'),
    path('permanent_deletion_org_release/<int:org_id>/<int:org_release_id>/', views_org_release.permanent_deletion_org_release, name='permanent_deletion_org_release'),
    path('restore_org_release/<int:org_id>/<int:org_release_id>/', views_org_release.restore_org_release, name='restore_org_release'),
    path('view_org_release/<int:org_id>/<int:org_release_id>/', views_org_release.view_org_release, name='view_org_release'),
    
    
    path('ajax_search_org_release_predecessors/', views_org_release.ajax_search_org_release_predecessors, name='ajax_search_org_release_predecessors'),
    
    path('create_org_global_release/<int:org_id>/', views_org_release.create_org_global_release, name='create_org_global_release'),
    path('create_org_release_with_iterations/<int:org_id>/', views_org_release.create_org_release_with_iterations, name='create_org_release_with_iterations'),
    
    
]
