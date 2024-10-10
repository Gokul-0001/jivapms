
from django.urls import path, include

from app_organization.mod_team import views_team


urlpatterns = [
    # app_organization/teams: DB/Model: Team
    path('list_teams/<int:org_id>/', views_team.list_teams, name='list_teams'),
    path('list_deleted_teams/<int:org_id>/', views_team.list_deleted_teams, name='list_deleted_teams'),
    path('create_team/<int:org_id>/', views_team.create_team, name='create_team'),
    path('edit_team/<int:org_id>/<int:team_id>/', views_team.edit_team, name='edit_team'),
    path('delete_team/<int:org_id>/<int:team_id>/', views_team.delete_team, name='delete_team'),
    path('permanent_deletion_team/<int:org_id>/<int:team_id>/', views_team.permanent_deletion_team, name='permanent_deletion_team'),
    path('restore_team/<int:org_id>/<int:team_id>/', views_team.restore_team, name='restore_team'),
    path('view_team/<int:org_id>/<int:team_id>/', views_team.view_team, name='view_team'),
]
