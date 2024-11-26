
from django.urls import path, include

from app_organization.mod_org_event import views_org_event


urlpatterns = [
    # app_organization/org_events: DB/Model: OrgEvent
    path('list_org_events/<int:org_id>/', views_org_event.list_org_events, name='list_org_events'),
    path('list_deleted_org_events/<int:org_id>/', views_org_event.list_deleted_org_events, name='list_deleted_org_events'),
    path('create_org_event/<int:org_id>/', views_org_event.create_org_event, name='create_org_event'),
    path('edit_org_event/<int:org_id>/<int:org_event_id>/', views_org_event.edit_org_event, name='edit_org_event'),
    path('delete_org_event/<int:org_id>/<int:org_event_id>/', views_org_event.delete_org_event, name='delete_org_event'),
    path('permanent_deletion_org_event/<int:org_id>/<int:org_event_id>/', views_org_event.permanent_deletion_org_event, name='permanent_deletion_org_event'),
    path('restore_org_event/<int:org_id>/<int:org_event_id>/', views_org_event.restore_org_event, name='restore_org_event'),
    path('view_org_event/<int:org_id>/<int:org_event_id>/', views_org_event.view_org_event, name='view_org_event'),
]
