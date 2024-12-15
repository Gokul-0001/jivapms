
from django.urls import path, include

from app_organization.mod_collection import views_collection


urlpatterns = [
    # app_organization/collections: DB/Model: Collection
    path('list_collections/<int:project_id>/', views_collection.list_collections, name='list_collections'),
    path('list_deleted_collections/<int:project_id>/', views_collection.list_deleted_collections, name='list_deleted_collections'),
    path('create_collection/<int:project_id>/', views_collection.create_collection, name='create_collection'),
    path('edit_collection/<int:project_id>/<int:collection_id>/', views_collection.edit_collection, name='edit_collection'),
    path('delete_collection/<int:project_id>/<int:collection_id>/', views_collection.delete_collection, name='delete_collection'),
    path('permanent_deletion_collection/<int:project_id>/<int:collection_id>/', views_collection.permanent_deletion_collection, name='permanent_deletion_collection'),
    path('restore_collection/<int:project_id>/<int:collection_id>/', views_collection.restore_collection, name='restore_collection'),
    path('view_collection/<int:project_id>/<int:collection_id>/', views_collection.view_collection, name='view_collection'),
]
