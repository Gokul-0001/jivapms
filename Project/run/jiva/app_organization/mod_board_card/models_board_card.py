
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project_board.models_project_board import *
from app_common.mod_common.models_common import *

class BoardCard(BaseModelImpl):
    project_board = models.OneToOneField('app_organization.ProjectBoard', on_delete=models.CASCADE, 
                            related_name="project_board_board_cards", null=True, blank=True)
    
    # Basic attributes for card settings
    display_card_id = models.BooleanField(default=True)
    display_card_size = models.BooleanField(default=True)
    display_card_priority = models.BooleanField(default=True)
    display_card_project = models.BooleanField(default=True)    
    display_card_iteration = models.BooleanField(default=True)

    display_card_assignee = models.BooleanField(default=False)
    display_card_release = models.BooleanField(default=False)    
    display_card_status = models.BooleanField(default=False)
    display_card_type = models.BooleanField(default=False)
    display_card_aging = models.BooleanField(default=False)
    display_card_due_date = models.BooleanField(default=False)
    display_card_summary = models.BooleanField(default=False)

    display_card_blocked = models.BooleanField(default=False)
    display_card_approved = models.BooleanField(default=False)
    display_card_done = models.BooleanField(default=False)

    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_cards")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
