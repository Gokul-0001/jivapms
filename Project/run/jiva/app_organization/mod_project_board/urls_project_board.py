
from django.urls import path, include

from app_organization.mod_project_board import views_project_board


urlpatterns = [
    # app_organization/project_boards: DB/Model: ProjectBoard
    path('list_project_boards/<int:project_id>/', views_project_board.list_project_boards, name='list_project_boards'),
    path('list_deleted_project_boards/<int:project_id>/', views_project_board.list_deleted_project_boards, name='list_deleted_project_boards'),
    path('create_project_board/<int:project_id>/', views_project_board.create_project_board, name='create_project_board'),
    path('edit_project_board/<int:project_id>/<int:project_board_id>/', views_project_board.edit_project_board, name='edit_project_board'),
    path('delete_project_board/<int:project_id>/<int:project_board_id>/', views_project_board.delete_project_board, name='delete_project_board'),
    path('permanent_deletion_project_board/<int:project_id>/<int:project_board_id>/', views_project_board.permanent_deletion_project_board, name='permanent_deletion_project_board'),
    path('restore_project_board/<int:project_id>/<int:project_board_id>/', views_project_board.restore_project_board, name='restore_project_board'),
    path('view_project_board/<int:project_id>/<int:project_board_id>/', views_project_board.view_project_board, name='view_project_board'),
]
