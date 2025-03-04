
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *



# this is the created code 
class ProjectBoard(BaseModelTrackDateImpl):
    # ref as of 08012025 DEFAULT_BOARD_COLUMNS = ['To Do', 'WIP', 'Done']
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="project_org_boards", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                                related_name="project_boards", null=True, blank=True)
    
    
    
    org_release = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, related_name="org_release_boards", null=True, blank=True)
    org_iteration = models.ForeignKey('app_organization.OrgIteration', on_delete=models.CASCADE, related_name="org_iteration_boards", null=True, blank=True)
    default_board = models.BooleanField(default=False)

    BOARD_TYPE_CHOICES = (
        ('TODO_WIP_DONE', 'To Do, WIP, Done'),
        ('KANBAN', 'To Do, Doing, Done'),
        ('SCRUM', 'To Do, WIP, Done'),
        ('Portfolio', 'Portfolio'),
        ('Program', 'Program'),
        ('Project', 'Project'),
    )
    board_type = models.CharField(max_length=50, choices=BOARD_TYPE_CHOICES, default='TODO_WIP_DONE')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_boards")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)






############# this is the default code #############

# class ProjectBoard(BaseModelImpl):
#     project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
#                             related_name="project_project_boards", null=True, blank=True)
    
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
#                                related_name="author_project_boards")
   
        
#     def __str__(self):
#         if self.name:
#             return self.name
#         else:
#             return str(self.id)
