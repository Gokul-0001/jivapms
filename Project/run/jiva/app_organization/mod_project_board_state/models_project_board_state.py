
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project_board.models_project_board import *
from app_common.mod_common.models_common import *

# this is the created code 
class ProjectBoardState(BaseModelTrackDateImpl):
    
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                                related_name="board_states", null=True, blank=True)
    
    wip_limit = models.PositiveIntegerField(default=0)

    buffer_column = models.BooleanField(default=False)
    COLUMN_TYPE_CHOICES = [
        ('To Do', 'To Do'),
        ('WIP', 'WIP'),
        ('Done', 'Done'),]
    column_type = models.CharField(max_length=10, choices=COLUMN_TYPE_CHOICES, default='To Do')  

    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_states")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


# this is the default code

# class ProjectBoardState(BaseModelImpl):
#     project_board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE, 
#                             related_name="project_board_project_board_states", null=True, blank=True)
    
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
#                                related_name="author_project_board_states")
   
        
#     def __str__(self):
#         if self.name:
#             return self.name
#         else:
#             return str(self.id)
