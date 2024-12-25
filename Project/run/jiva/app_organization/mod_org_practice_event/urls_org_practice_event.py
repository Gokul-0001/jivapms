
from django.urls import path, include

from app_organization.mod_org_practice_event import views_org_practice_event


urlpatterns = [
    # app_organization/org_practice_events: DB/Model: OrgPracticeEvent
    path('list_org_practice_events/<int:org_event_id>/', views_org_practice_event.list_org_practice_events, name='list_org_practice_events'),
    path('list_deleted_org_practice_events/<int:org_event_id>/', views_org_practice_event.list_deleted_org_practice_events, name='list_deleted_org_practice_events'),
    path('create_org_practice_event/<int:org_event_id>/', views_org_practice_event.create_org_practice_event, name='create_org_practice_event'),
    path('edit_org_practice_event/<int:org_event_id>/<int:org_practice_event_id>/', views_org_practice_event.edit_org_practice_event, name='edit_org_practice_event'),
    path('delete_org_practice_event/<int:org_event_id>/<int:org_practice_event_id>/', views_org_practice_event.delete_org_practice_event, name='delete_org_practice_event'),
    path('permanent_deletion_org_practice_event/<int:org_event_id>/<int:org_practice_event_id>/', views_org_practice_event.permanent_deletion_org_practice_event, name='permanent_deletion_org_practice_event'),
    path('restore_org_practice_event/<int:org_event_id>/<int:org_practice_event_id>/', views_org_practice_event.restore_org_practice_event, name='restore_org_practice_event'),
    path('view_org_practice_event/<int:org_event_id>/<int:org_practice_event_id>/', views_org_practice_event.view_org_practice_event, name='view_org_practice_event'),
]
