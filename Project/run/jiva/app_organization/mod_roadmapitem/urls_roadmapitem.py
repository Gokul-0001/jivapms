
from django.urls import path, include

from app_organization.mod_roadmapitem import views_roadmapitem


urlpatterns = [
    # app_organization/roadmapitems: DB/Model: Roadmapitem
    path('list_roadmapitems/<int:org_id>/', views_roadmapitem.list_roadmapitems, name='list_roadmapitems'),
    path('list_deleted_roadmapitems/<int:org_id>/', views_roadmapitem.list_deleted_roadmapitems, name='list_deleted_roadmapitems'),
    path('create_roadmapitem/<int:org_id>/', views_roadmapitem.create_roadmapitem, name='create_roadmapitem'),
    path('edit_roadmapitem/<int:org_id>/<int:roadmapitem_id>/', views_roadmapitem.edit_roadmapitem, name='edit_roadmapitem'),
    path('delete_roadmapitem/<int:org_id>/<int:roadmapitem_id>/', views_roadmapitem.delete_roadmapitem, name='delete_roadmapitem'),
    path('permanent_deletion_roadmapitem/<int:org_id>/<int:roadmapitem_id>/', views_roadmapitem.permanent_deletion_roadmapitem, name='permanent_deletion_roadmapitem'),
    path('restore_roadmapitem/<int:org_id>/<int:roadmapitem_id>/', views_roadmapitem.restore_roadmapitem, name='restore_roadmapitem'),
    path('view_roadmapitem/<int:org_id>/<int:roadmapitem_id>/', views_roadmapitem.view_roadmapitem, name='view_roadmapitem'),
]
