
from django.urls import path, include

from app_organization.mod_project_board_swimlane import views_project_board_swimlane


urlpatterns = [
    # app_organization/project_board_swimlanes: DB/Model: ProjectBoardSwimlane
    path('list_project_board_swimlanes/<int:project_id>/', views_project_board_swimlane.list_project_board_swimlanes, name='list_project_board_swimlanes'),
    path('list_deleted_project_board_swimlanes/<int:project_id>/', views_project_board_swimlane.list_deleted_project_board_swimlanes, name='list_deleted_project_board_swimlanes'),
    path('create_project_board_swimlane/<int:project_id>/', views_project_board_swimlane.create_project_board_swimlane, name='create_project_board_swimlane'),
    path('edit_project_board_swimlane/<int:project_id>/<int:project_board_swimlane_id>/', views_project_board_swimlane.edit_project_board_swimlane, name='edit_project_board_swimlane'),
    path('delete_project_board_swimlane/<int:project_id>/<int:project_board_swimlane_id>/', views_project_board_swimlane.delete_project_board_swimlane, name='delete_project_board_swimlane'),
    path('permanent_deletion_project_board_swimlane/<int:project_id>/<int:project_board_swimlane_id>/', views_project_board_swimlane.permanent_deletion_project_board_swimlane, name='permanent_deletion_project_board_swimlane'),
    path('restore_project_board_swimlane/<int:project_id>/<int:project_board_swimlane_id>/', views_project_board_swimlane.restore_project_board_swimlane, name='restore_project_board_swimlane'),
    path('view_project_board_swimlane/<int:project_id>/<int:project_board_swimlane_id>/', views_project_board_swimlane.view_project_board_swimlane, name='view_project_board_swimlane'),
]
