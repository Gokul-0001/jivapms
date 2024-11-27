
from django.urls import path, include

from app_organization.mod_org_image_map import views_org_image_map


urlpatterns = [
    # app_organization/org_image_maps: DB/Model: OrgImageMap
    path('list_org_image_maps/<int:organization_id>/', views_org_image_map.list_org_image_maps, name='list_org_image_maps'),
    path('list_deleted_org_image_maps/<int:organization_id>/', views_org_image_map.list_deleted_org_image_maps, name='list_deleted_org_image_maps'),
    path('create_org_image_map/<int:organization_id>/', views_org_image_map.create_org_image_map, name='create_org_image_map'),
    path('edit_org_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.edit_org_image_map, name='edit_org_image_map'),
    path('delete_org_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.delete_org_image_map, name='delete_org_image_map'),
    path('permanent_deletion_org_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.permanent_deletion_org_image_map, name='permanent_deletion_org_image_map'),
    path('restore_org_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.restore_org_image_map, name='restore_org_image_map'),
    path('view_org_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.view_org_image_map, name='view_org_image_map'),
    
    path('image_map_editor/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.image_map_editor, name='image_map_editor'),
    path('view_visual_image_map/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.view_visual_image_map, name='view_visual_image_map'),
    path('generate_visual_image_map_code/<int:organization_id>/<int:org_image_map_id>/', views_org_image_map.generate_visual_image_map_code, name='generate_visual_image_map_code'),
    path('delete_area/<int:area_id>/', views_org_image_map.delete_area, name='delete_area'),
    path('update_area/<int:area_id>/', views_org_image_map.update_area, name='update_area'),    
    
    path('display_visual_image_map/<int:organization_id>/<int:org_image_map_id>/<int:framework_id>/', views_org_image_map.display_visual_image_map, name='display_visual_image_map'),
]
