
from django.urls import path, include

from app_organization.mod_org_team import views_org_team


urlpatterns = [
    # app_organization/org_teams: DB/Model: OrgTeam
    path('list_org_teams/<int:org_id>/', views_org_team.list_org_teams, name='list_org_teams'),
    path('list_deleted_org_teams/<int:org_id>/', views_org_team.list_deleted_org_teams, name='list_deleted_org_teams'),
    path('create_org_team/<int:org_id>/', views_org_team.create_org_team, name='create_org_team'),
    path('edit_org_team/<int:org_id>/<int:org_team_id>/', views_org_team.edit_org_team, name='edit_org_team'),
    path('delete_org_team/<int:org_id>/<int:org_team_id>/', views_org_team.delete_org_team, name='delete_org_team'),
    path('permanent_deletion_org_team/<int:org_id>/<int:org_team_id>/', views_org_team.permanent_deletion_org_team, name='permanent_deletion_org_team'),
    path('restore_org_team/<int:org_id>/<int:org_team_id>/', views_org_team.restore_org_team, name='restore_org_team'),
    path('view_org_team/<int:org_id>/<int:org_team_id>/', views_org_team.view_org_team, name='view_org_team'),
]
