
from django.urls import path, include

from app_organization.mod_metric import views_metric


urlpatterns = [
    # app_organization/metrics: DB/Model: Metric
    path('list_metrics/<int:pro_id>/', views_metric.list_metrics, name='list_metrics'),
    path('list_deleted_metrics/<int:pro_id>/', views_metric.list_deleted_metrics, name='list_deleted_metrics'),
    path('create_metric/<int:pro_id>/', views_metric.create_metric, name='create_metric'),
    path('edit_metric/<int:pro_id>/<int:metric_id>/', views_metric.edit_metric, name='edit_metric'),
    path('delete_metric/<int:pro_id>/<int:metric_id>/', views_metric.delete_metric, name='delete_metric'),
    path('permanent_deletion_metric/<int:pro_id>/<int:metric_id>/', views_metric.permanent_deletion_metric, name='permanent_deletion_metric'),
    path('restore_metric/<int:pro_id>/<int:metric_id>/', views_metric.restore_metric, name='restore_metric'),
    path('view_metric/<int:pro_id>/<int:metric_id>/', views_metric.view_metric, name='view_metric'),
]
