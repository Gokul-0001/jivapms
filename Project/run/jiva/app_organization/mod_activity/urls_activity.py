
from django.urls import path, include

from app_organization.mod_activity import views_activity


urlpatterns = [
    # app_organization/activities: DB/Model: Activity
    path('list_activities/<int:persona_id>/', views_activity.list_activities, name='list_activities'),
    path('list_deleted_activities/<int:persona_id>/', views_activity.list_deleted_activities, name='list_deleted_activities'),
    path('create_activity/<int:persona_id>/', views_activity.create_activity, name='create_activity'),
    path('edit_activity/<int:persona_id>/<int:activity_id>/', views_activity.edit_activity, name='edit_activity'),
    path('delete_activity/<int:persona_id>/<int:activity_id>/', views_activity.delete_activity, name='delete_activity'),
    path('permanent_deletion_activity/<int:persona_id>/<int:activity_id>/', views_activity.permanent_deletion_activity, name='permanent_deletion_activity'),
    path('restore_activity/<int:persona_id>/<int:activity_id>/', views_activity.restore_activity, name='restore_activity'),
    path('view_activity/<int:persona_id>/<int:activity_id>/', views_activity.view_activity, name='view_activity'),
]
