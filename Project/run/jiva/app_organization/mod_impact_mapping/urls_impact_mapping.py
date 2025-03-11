
from django.urls import path, include

from app_organization.mod_impact_mapping import views_impact_mapping


urlpatterns = [
    # app_organization/impact_mappings: DB/Model: ImpactMapping
    path('list_impact_mappings/<int:organization_id>/', views_impact_mapping.list_impact_mappings, name='list_impact_mappings'),
    path('list_deleted_impact_mappings/<int:organization_id>/', views_impact_mapping.list_deleted_impact_mappings, name='list_deleted_impact_mappings'),
    path('create_impact_mapping/<int:organization_id>/', views_impact_mapping.create_impact_mapping, name='create_impact_mapping'),
    path('edit_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.edit_impact_mapping, name='edit_impact_mapping'),
    path('delete_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.delete_impact_mapping, name='delete_impact_mapping'),
    path('permanent_deletion_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.permanent_deletion_impact_mapping, name='permanent_deletion_impact_mapping'),
    path('restore_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.restore_impact_mapping, name='restore_impact_mapping'),
    path('view_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.view_impact_mapping, name='view_impact_mapping'),
    
    path('editor_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.editor_impact_mapping, name='editor_impact_mapping'),
    path('view_tree_table_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.view_tree_table_mapping, name='view_tree_table_mapping'),
    
    path('ajax_save_impact_mappings/', views_impact_mapping.ajax_save_impact_mappings, name='ajax_save_impact_mappings'),

    path('editor_horizontal_impact_mapping/<int:organization_id>/<int:impact_mapping_id>/', views_impact_mapping.editor_horizontal_impact_mapping, name='editor_horizontal_impact_mapping'),

    path('ajax_impact_mapping_add_node/', views_impact_mapping.ajax_impact_mapping_add_node, name='ajax_impact_mapping_add_node'),
    path('ajax_impact_mapping_delete_node/', views_impact_mapping.ajax_impact_mapping_delete_node, name='ajax_impact_mapping_delete_node'),
]
