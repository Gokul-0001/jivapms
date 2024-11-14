
from django.urls import path, include

from app_organization.mod_dev_value_stream import views_dev_value_stream


urlpatterns = [
    # app_organization/dev_value_streams: DB/Model: DevValueStream
    path('list_dev_value_streams/<int:ops_id>/', views_dev_value_stream.list_dev_value_streams, name='list_dev_value_streams'),
    path('list_deleted_dev_value_streams/<int:ops_id>/', views_dev_value_stream.list_deleted_dev_value_streams, name='list_deleted_dev_value_streams'),
    path('create_dev_value_stream/<int:ops_id>/', views_dev_value_stream.create_dev_value_stream, name='create_dev_value_stream'),
    path('edit_dev_value_stream/<int:ops_id>/<int:dev_value_stream_id>/', views_dev_value_stream.edit_dev_value_stream, name='edit_dev_value_stream'),
    path('delete_dev_value_stream/<int:ops_id>/<int:dev_value_stream_id>/', views_dev_value_stream.delete_dev_value_stream, name='delete_dev_value_stream'),
    path('permanent_deletion_dev_value_stream/<int:ops_id>/<int:dev_value_stream_id>/', views_dev_value_stream.permanent_deletion_dev_value_stream, name='permanent_deletion_dev_value_stream'),
    path('restore_dev_value_stream/<int:ops_id>/<int:dev_value_stream_id>/', views_dev_value_stream.restore_dev_value_stream, name='restore_dev_value_stream'),
    path('view_dev_value_stream/<int:ops_id>/<int:dev_value_stream_id>/', views_dev_value_stream.view_dev_value_stream, name='view_dev_value_stream'),
]
