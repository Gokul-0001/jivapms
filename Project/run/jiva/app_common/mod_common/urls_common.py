from django.urls import path, include

from app_common.mod_common import views_common

# purpose: common services for all apps
# caution: need to have imports of all models and forms from all apps

urlpatterns = [
    path('ajax_update_model_list_sorted/', views_common.ajax_update_model_list_sorted, name='ajax_update_model_list_sorted'),
    path('ajax_save_element_text/', views_common.ajax_save_element_text, name='ajax_save_element_text'),
    path('ajax_update_task_done_state/', views_common.ajax_update_task_done_state, name='ajax_update_task_done_state'),
    path('ajax_save_related_model/', views_common.ajax_save_related_model, name='ajax_save_related_model'),
    path('ajax_create_child_element/', views_common.ajax_create_child_element, name='ajax_create_child_element'),
    path('ajax_create_record/', views_common.ajax_create_record, name='ajax_create_record'),
    
    
    
    path('ajax_update_row_task_done_state/', views_common.ajax_update_row_task_done_state, name='ajax_update_row_task_done_state'),

    path('ajax_update_checkbox_state/', views_common.ajax_update_checkbox_state, name='ajax_update_checkbox_state'),
    path('ajax_update_select_box/', views_common.ajax_update_select_box, name='ajax_update_select_box'),
    path('ajax_update_default_radio_box/', views_common.ajax_update_default_radio_box, name='ajax_update_default_radio_box'),
    
]
