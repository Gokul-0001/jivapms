
from django.urls import path, include

from app_organization.mod_iteration import views_iteration


urlpatterns = [
    # app_organization/iterations: DB/Model: Iteration
    path('list_iterations/<int:rel_id>/', views_iteration.list_iterations, name='list_iterations'),
    path('list_deleted_iterations/<int:rel_id>/', views_iteration.list_deleted_iterations, name='list_deleted_iterations'),
    path('create_iteration/<int:rel_id>/', views_iteration.create_iteration, name='create_iteration'),
    path('edit_iteration/<int:rel_id>/<int:iteration_id>/', views_iteration.edit_iteration, name='edit_iteration'),
    path('delete_iteration/<int:rel_id>/<int:iteration_id>/', views_iteration.delete_iteration, name='delete_iteration'),
    path('permanent_deletion_iteration/<int:rel_id>/<int:iteration_id>/', views_iteration.permanent_deletion_iteration, name='permanent_deletion_iteration'),
    path('restore_iteration/<int:rel_id>/<int:iteration_id>/', views_iteration.restore_iteration, name='restore_iteration'),
    path('view_iteration/<int:rel_id>/<int:iteration_id>/', views_iteration.view_iteration, name='view_iteration'),
]
