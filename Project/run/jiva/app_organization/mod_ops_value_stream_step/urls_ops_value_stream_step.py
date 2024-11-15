
from django.urls import path, include

from app_organization.mod_ops_value_stream_step import views_ops_value_stream_step


urlpatterns = [
    # app_organization/ops_value_stream_steps: DB/Model: OpsValueStreamStep
    path('list_ops_value_stream_steps/<int:ops_id>/', views_ops_value_stream_step.list_ops_value_stream_steps, name='list_ops_value_stream_steps'),
    path('list_deleted_ops_value_stream_steps/<int:ops_id>/', views_ops_value_stream_step.list_deleted_ops_value_stream_steps, name='list_deleted_ops_value_stream_steps'),
    path('create_ops_value_stream_step/<int:ops_id>/', views_ops_value_stream_step.create_ops_value_stream_step, name='create_ops_value_stream_step'),
    path('add_ops_value_stream_step/<int:ops_id>/', views_ops_value_stream_step.add_ops_value_stream_step, name='add_ops_value_stream_step'),
    path('edit_ops_value_stream_step/<int:ops_id>/<int:ops_value_stream_step_id>/', views_ops_value_stream_step.edit_ops_value_stream_step, name='edit_ops_value_stream_step'),
    path('delete_ops_value_stream_step/<int:ops_id>/<int:ops_value_stream_step_id>/', views_ops_value_stream_step.delete_ops_value_stream_step, name='delete_ops_value_stream_step'),
    path('permanent_deletion_ops_value_stream_step/<int:ops_id>/<int:ops_value_stream_step_id>/', views_ops_value_stream_step.permanent_deletion_ops_value_stream_step, name='permanent_deletion_ops_value_stream_step'),
    path('restore_ops_value_stream_step/<int:ops_id>/<int:ops_value_stream_step_id>/', views_ops_value_stream_step.restore_ops_value_stream_step, name='restore_ops_value_stream_step'),
    path('view_ops_value_stream_step/<int:ops_id>/<int:ops_value_stream_step_id>/', views_ops_value_stream_step.view_ops_value_stream_step, name='view_ops_value_stream_step'),
]
