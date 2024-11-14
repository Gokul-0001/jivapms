
from django.urls import path, include

from app_organization.mod_dev_value_stream_step import views_dev_value_stream_step


urlpatterns = [
    # app_organization/dev_value_stream_steps: DB/Model: DevValueStreamStep
    path('list_dev_value_stream_steps/<int:dev_id>/', views_dev_value_stream_step.list_dev_value_stream_steps, name='list_dev_value_stream_steps'),
    path('list_deleted_dev_value_stream_steps/<int:dev_id>/', views_dev_value_stream_step.list_deleted_dev_value_stream_steps, name='list_deleted_dev_value_stream_steps'),
    path('create_dev_value_stream_step/<int:dev_id>/', views_dev_value_stream_step.create_dev_value_stream_step, name='create_dev_value_stream_step'),
    path('edit_dev_value_stream_step/<int:dev_id>/<int:dev_value_stream_step_id>/', views_dev_value_stream_step.edit_dev_value_stream_step, name='edit_dev_value_stream_step'),
    path('delete_dev_value_stream_step/<int:dev_id>/<int:dev_value_stream_step_id>/', views_dev_value_stream_step.delete_dev_value_stream_step, name='delete_dev_value_stream_step'),
    path('permanent_deletion_dev_value_stream_step/<int:dev_id>/<int:dev_value_stream_step_id>/', views_dev_value_stream_step.permanent_deletion_dev_value_stream_step, name='permanent_deletion_dev_value_stream_step'),
    path('restore_dev_value_stream_step/<int:dev_id>/<int:dev_value_stream_step_id>/', views_dev_value_stream_step.restore_dev_value_stream_step, name='restore_dev_value_stream_step'),
    path('view_dev_value_stream_step/<int:dev_id>/<int:dev_value_stream_step_id>/', views_dev_value_stream_step.view_dev_value_stream_step, name='view_dev_value_stream_step'),
]
