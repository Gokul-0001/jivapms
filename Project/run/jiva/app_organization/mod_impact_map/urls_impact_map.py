
from django.urls import path, include

from app_organization.mod_impact_map import views_impact_map


urlpatterns = [
    # app_organization/impact_maps: DB/Model: ImpactMap
    path('list_impact_maps/<int:impact_mapping_id>/', views_impact_map.list_impact_maps, name='list_impact_maps'),
    path('list_deleted_impact_maps/<int:impact_mapping_id>/', views_impact_map.list_deleted_impact_maps, name='list_deleted_impact_maps'),
    path('create_impact_map/<int:impact_mapping_id>/', views_impact_map.create_impact_map, name='create_impact_map'),
    path('edit_impact_map/<int:impact_mapping_id>/<int:impact_map_id>/', views_impact_map.edit_impact_map, name='edit_impact_map'),
    path('delete_impact_map/<int:impact_mapping_id>/<int:impact_map_id>/', views_impact_map.delete_impact_map, name='delete_impact_map'),
    path('permanent_deletion_impact_map/<int:impact_mapping_id>/<int:impact_map_id>/', views_impact_map.permanent_deletion_impact_map, name='permanent_deletion_impact_map'),
    path('restore_impact_map/<int:impact_mapping_id>/<int:impact_map_id>/', views_impact_map.restore_impact_map, name='restore_impact_map'),
    path('view_impact_map/<int:impact_mapping_id>/<int:impact_map_id>/', views_impact_map.view_impact_map, name='view_impact_map'),
]
