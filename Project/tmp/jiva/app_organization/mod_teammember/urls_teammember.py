
from django.urls import path, include

from app_organization.mod_teammember import views_teammember


urlpatterns = [
    # app_organization/teammembers: DB/Model: Teammember
    path('list_teammembers/<int:tea_id>/', views_teammember.list_teammembers, name='list_teammembers'),
    path('list_deleted_teammembers/<int:tea_id>/', views_teammember.list_deleted_teammembers, name='list_deleted_teammembers'),
    path('create_teammember/<int:tea_id>/', views_teammember.create_teammember, name='create_teammember'),
    path('edit_teammember/<int:tea_id>/<int:teammember_id>/', views_teammember.edit_teammember, name='edit_teammember'),
    path('delete_teammember/<int:tea_id>/<int:teammember_id>/', views_teammember.delete_teammember, name='delete_teammember'),
    path('permanent_deletion_teammember/<int:tea_id>/<int:teammember_id>/', views_teammember.permanent_deletion_teammember, name='permanent_deletion_teammember'),
    path('restore_teammember/<int:tea_id>/<int:teammember_id>/', views_teammember.restore_teammember, name='restore_teammember'),
    path('view_teammember/<int:tea_id>/<int:teammember_id>/', views_teammember.view_teammember, name='view_teammember'),
]
