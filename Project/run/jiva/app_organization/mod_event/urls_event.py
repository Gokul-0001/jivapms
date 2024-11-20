
from django.urls import path, include

from app_organization.mod_event import views_event


urlpatterns = [
    # app_organization/events: DB/Model: Event
    path('list_events/<int:pro_id>/', views_event.list_events, name='list_events'),
    path('list_deleted_events/<int:pro_id>/', views_event.list_deleted_events, name='list_deleted_events'),
    path('create_event/<int:pro_id>/', views_event.create_event, name='create_event'),
    path('edit_event/<int:pro_id>/<int:event_id>/', views_event.edit_event, name='edit_event'),
    path('delete_event/<int:pro_id>/<int:event_id>/', views_event.delete_event, name='delete_event'),
    path('permanent_deletion_event/<int:pro_id>/<int:event_id>/', views_event.permanent_deletion_event, name='permanent_deletion_event'),
    path('restore_event/<int:pro_id>/<int:event_id>/', views_event.restore_event, name='restore_event'),
    path('view_event/<int:pro_id>/<int:event_id>/', views_event.view_event, name='view_event'),
]
