
from django.urls import path, include

from app_organization.mod_org_metric import views_org_metric


urlpatterns = [
    # app_organization/org_metrics: DB/Model: OrgMetric
    path('list_org_metrics/<int:org_id>/', views_org_metric.list_org_metrics, name='list_org_metrics'),
    path('list_deleted_org_metrics/<int:org_id>/', views_org_metric.list_deleted_org_metrics, name='list_deleted_org_metrics'),
    path('create_org_metric/<int:org_id>/', views_org_metric.create_org_metric, name='create_org_metric'),
    path('edit_org_metric/<int:org_id>/<int:org_metric_id>/', views_org_metric.edit_org_metric, name='edit_org_metric'),
    path('delete_org_metric/<int:org_id>/<int:org_metric_id>/', views_org_metric.delete_org_metric, name='delete_org_metric'),
    path('permanent_deletion_org_metric/<int:org_id>/<int:org_metric_id>/', views_org_metric.permanent_deletion_org_metric, name='permanent_deletion_org_metric'),
    path('restore_org_metric/<int:org_id>/<int:org_metric_id>/', views_org_metric.restore_org_metric, name='restore_org_metric'),
    path('view_org_metric/<int:org_id>/<int:org_metric_id>/', views_org_metric.view_org_metric, name='view_org_metric'),
    
    # added
    path('view_project_metrics/<int:project_id>/', views_org_metric.view_project_metrics, name='view_project_metrics'),
    path('view_project_metrics_backlog_tab/<int:project_id>/', 
         views_org_metric.view_project_metrics_backlog_tab, name='view_project_metrics_backlog_tab'),
    path('view_project_metrics_iteration_tab/<int:project_id>/', views_org_metric.view_project_metrics_iteration_tab, name='view_project_metrics_iteration_tab'),
    path('view_project_metrics_quality_tab/<int:project_id>/', views_org_metric.view_project_metrics_quality_tab, 
         name='view_project_metrics_quality_tab'),
    path('view_project_metrics_release_tab/<int:project_id>/', views_org_metric.view_project_metrics_release_tab, 
         name='view_project_metrics_release_tab'),
]
