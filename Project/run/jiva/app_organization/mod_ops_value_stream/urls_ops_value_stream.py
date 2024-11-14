
from django.urls import path, include

from app_organization.mod_ops_value_stream import views_ops_value_stream


urlpatterns = [
    # app_organization/ops_value_streams: DB/Model: OpsValueStream
    path('list_ops_value_streams/<int:org_id>/', views_ops_value_stream.list_ops_value_streams, name='list_ops_value_streams'),
    path('list_deleted_ops_value_streams/<int:org_id>/', views_ops_value_stream.list_deleted_ops_value_streams, name='list_deleted_ops_value_streams'),
    path('create_ops_value_stream/<int:org_id>/', views_ops_value_stream.create_ops_value_stream, name='create_ops_value_stream'),
    path('edit_ops_value_stream/<int:org_id>/<int:ops_value_stream_id>/', views_ops_value_stream.edit_ops_value_stream, name='edit_ops_value_stream'),
    path('delete_ops_value_stream/<int:org_id>/<int:ops_value_stream_id>/', views_ops_value_stream.delete_ops_value_stream, name='delete_ops_value_stream'),
    path('permanent_deletion_ops_value_stream/<int:org_id>/<int:ops_value_stream_id>/', views_ops_value_stream.permanent_deletion_ops_value_stream, name='permanent_deletion_ops_value_stream'),
    path('restore_ops_value_stream/<int:org_id>/<int:ops_value_stream_id>/', views_ops_value_stream.restore_ops_value_stream, name='restore_ops_value_stream'),
    path('view_ops_value_stream/<int:org_id>/<int:ops_value_stream_id>/', views_ops_value_stream.view_ops_value_stream, name='view_ops_value_stream'),
]
