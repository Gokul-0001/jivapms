
from django.urls import path, include

from app_organization.mod_image_map import views_image_map


urlpatterns = [
    # app_organization/image_maps: DB/Model: ImageMap
    path('list_image_maps/<int:pro_id>/', views_image_map.list_image_maps, name='list_image_maps'),
    path('list_deleted_image_maps/<int:pro_id>/', views_image_map.list_deleted_image_maps, name='list_deleted_image_maps'),
    path('create_image_map/<int:pro_id>/', views_image_map.create_image_map, name='create_image_map'),
    path('edit_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.edit_image_map, name='edit_image_map'),
    path('image_map_editor/<int:pro_id>/<int:image_map_id>/', views_image_map.image_map_editor, name='image_map_editor'),
    path('delete_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.delete_image_map, name='delete_image_map'),
    path('permanent_deletion_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.permanent_deletion_image_map, name='permanent_deletion_image_map'),
    path('restore_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.restore_image_map, name='restore_image_map'),
    path('view_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.view_image_map, name='view_image_map'),
    path('view_visual_image_map/<int:pro_id>/<int:image_map_id>/', views_image_map.view_visual_image_map, name='view_visual_image_map'),
]
