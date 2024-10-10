
from django.urls import path, include

from app_organization.mod_projectmembership import views_projectmembership


urlpatterns = [
    # app_organization/projectmemberships: DB/Model: Projectmembership
    path('list_projectmemberships/<int:pro_id>/', views_projectmembership.list_projectmemberships, name='list_projectmemberships'),
    path('list_deleted_projectmemberships/<int:pro_id>/', views_projectmembership.list_deleted_projectmemberships, name='list_deleted_projectmemberships'),
    path('create_projectmembership/<int:pro_id>/', views_projectmembership.create_projectmembership, name='create_projectmembership'),
    path('edit_projectmembership/<int:pro_id>/<int:projectmembership_id>/', views_projectmembership.edit_projectmembership, name='edit_projectmembership'),
    path('delete_projectmembership/<int:pro_id>/<int:projectmembership_id>/', views_projectmembership.delete_projectmembership, name='delete_projectmembership'),
    path('permanent_deletion_projectmembership/<int:pro_id>/<int:projectmembership_id>/', views_projectmembership.permanent_deletion_projectmembership, name='permanent_deletion_projectmembership'),
    path('restore_projectmembership/<int:pro_id>/<int:projectmembership_id>/', views_projectmembership.restore_projectmembership, name='restore_projectmembership'),
    path('view_projectmembership/<int:pro_id>/<int:projectmembership_id>/', views_projectmembership.view_projectmembership, name='view_projectmembership'),
]
