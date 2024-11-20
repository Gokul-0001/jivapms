
from django.urls import path, include

from app_organization.mod_release import views_release


urlpatterns = [
    # app_organization/releases: DB/Model: Release
    path('list_releases/<int:pro_id>/', views_release.list_releases, name='list_releases'),
    path('list_deleted_releases/<int:pro_id>/', views_release.list_deleted_releases, name='list_deleted_releases'),
    path('create_release/<int:pro_id>/', views_release.create_release, name='create_release'),
    path('edit_release/<int:pro_id>/<int:release_id>/', views_release.edit_release, name='edit_release'),
    path('delete_release/<int:pro_id>/<int:release_id>/', views_release.delete_release, name='delete_release'),
    path('permanent_deletion_release/<int:pro_id>/<int:release_id>/', views_release.permanent_deletion_release, name='permanent_deletion_release'),
    path('restore_release/<int:pro_id>/<int:release_id>/', views_release.restore_release, name='restore_release'),
    path('view_release/<int:pro_id>/<int:release_id>/', views_release.view_release, name='view_release'),
]
