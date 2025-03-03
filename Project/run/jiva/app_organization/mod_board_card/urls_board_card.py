
from django.urls import path, include

from app_organization.mod_board_card import views_board_card


urlpatterns = [
    # app_organization/board_cards: DB/Model: BoardCard
    path('list_board_cards/<int:project_board_id>/', views_board_card.list_board_cards, name='list_board_cards'),
    path('list_deleted_board_cards/<int:project_board_id>/', views_board_card.list_deleted_board_cards, name='list_deleted_board_cards'),
    path('create_board_card/<int:project_board_id>/', views_board_card.create_board_card, name='create_board_card'),
    path('edit_board_card/<int:project_board_id>/<int:board_card_id>/', views_board_card.edit_board_card, name='edit_board_card'),
    path('delete_board_card/<int:project_board_id>/<int:board_card_id>/', views_board_card.delete_board_card, name='delete_board_card'),
    path('permanent_deletion_board_card/<int:project_board_id>/<int:board_card_id>/', views_board_card.permanent_deletion_board_card, name='permanent_deletion_board_card'),
    path('restore_board_card/<int:project_board_id>/<int:board_card_id>/', views_board_card.restore_board_card, name='restore_board_card'),
    path('view_board_card/<int:project_board_id>/<int:board_card_id>/', views_board_card.view_board_card, name='view_board_card'),

    path('board_card_settings/<int:project_board_id>/', views_board_card.board_card_settings, name='board_card_settings'),
]
