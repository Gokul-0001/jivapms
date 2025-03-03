
from django.urls import path, include

from app_organization.mod_project_board_state import views_project_board_state


urlpatterns = [
    # app_organization/project_board_states: DB/Model: ProjectBoardState
    path('list_project_board_states/<int:project_board_id>/', views_project_board_state.list_project_board_states, name='list_project_board_states'),
    path('list_deleted_project_board_states/<int:project_board_id>/', views_project_board_state.list_deleted_project_board_states, name='list_deleted_project_board_states'),
    path('create_project_board_state/<int:project_board_id>/', views_project_board_state.create_project_board_state, name='create_project_board_state'),
    path('edit_project_board_state/<int:project_board_id>/<int:project_board_state_id>/', views_project_board_state.edit_project_board_state, name='edit_project_board_state'),
    path('delete_project_board_state/<int:project_board_id>/<int:project_board_state_id>/', views_project_board_state.delete_project_board_state, name='delete_project_board_state'),
    path('permanent_deletion_project_board_state/<int:project_board_id>/<int:project_board_state_id>/', views_project_board_state.permanent_deletion_project_board_state, name='permanent_deletion_project_board_state'),
    path('restore_project_board_state/<int:project_board_id>/<int:project_board_state_id>/', views_project_board_state.restore_project_board_state, name='restore_project_board_state'),
    path('view_project_board_state/<int:project_board_id>/<int:project_board_state_id>/', views_project_board_state.view_project_board_state, name='view_project_board_state'),

    path('add_project_board_state/<int:project_board_id>/', views_project_board_state.add_project_board_state, name='add_project_board_state'),
]
