
from django.urls import path, include

from app_organization.mod_board import views_board


urlpatterns = [
    # app_organization/boards: DB/Model: Board
    path('list_boards/<int:pro_id>/', views_board.list_boards, name='list_boards'),
    path('list_deleted_boards/<int:pro_id>/', views_board.list_deleted_boards, name='list_deleted_boards'),
    path('create_board/<int:pro_id>/', views_board.create_board, name='create_board'),
    path('edit_board/<int:pro_id>/<int:board_id>/', views_board.edit_board, name='edit_board'),
    path('delete_board/<int:pro_id>/<int:board_id>/', views_board.delete_board, name='delete_board'),
    path('permanent_deletion_board/<int:pro_id>/<int:board_id>/', views_board.permanent_deletion_board, name='permanent_deletion_board'),
    path('restore_board/<int:pro_id>/<int:board_id>/', views_board.restore_board, name='restore_board'),
    path('view_board/<int:pro_id>/<int:board_id>/', views_board.view_board, name='view_board'),
]
