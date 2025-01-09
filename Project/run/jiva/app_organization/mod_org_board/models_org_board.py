
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *   
from app_common.mod_common.models_common import *

class OrgBoard(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_boards", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                                related_name="org_project_boards", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_boards")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


class ProjectBoard(BaseModelTrackDateImpl):
    # ref as of 08012025 DEFAULT_BOARD_COLUMNS = ['To Do', 'WIP', 'Done']
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="project_org_boards", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                                related_name="project_boards", null=True, blank=True)
    

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_boards")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


class ProjectBoardState(BaseModelTrackDateImpl):
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                                related_name="board_states", null=True, blank=True)
    
    wip_limit = models.PositiveIntegerField(default=0)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_states")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)

class ProjectBoardStateTransition(BaseModelTrackDateImpl):
    card = models.ForeignKey('app_organization.Backlog', on_delete=models.CASCADE,null=True, blank=True,
                               related_name="card_transitions")
                             
                             
    from_state = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transitions_from"
    )
    to_state = models.ForeignKey(
        'app_organization.ProjectBoardState',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transitions_to"
    )
    transition_time = models.DateTimeField(auto_now_add=True, null=True,
        blank=True)
    
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who moved the card
    notes = models.TextField(null=True, blank=True)  # Optional transition notes

    def __str__(self):
        return f"Transition of Card {self.card.id}: {self.from_state} → {self.to_state} at {self.transition_time}"


class ProjectBoardCard(BaseModelTrackDateImpl):
    backlog = models.ForeignKey('app_organization.Backlog', on_delete=models.CASCADE, related_name="board_cards", null=True, blank=True)
    board = models.ForeignKey(ProjectBoard, on_delete=models.CASCADE, related_name="board_cards", null=True, blank=True)
    state = models.ForeignKey(ProjectBoardState, on_delete=models.CASCADE, related_name="state_cards", null=True, blank=True)
    swimlane = models.ForeignKey(
        'app_organization.ProjectBoardSwimLane', on_delete=models.SET_NULL, null=True, blank=True, related_name="swimlane_cards"
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['board', 'state']),
        ]
    def __str__(self):
        if self.backlog.name:
            return self.backlog.name
        else:
            return str(self.id)

class ProjectBoardSwimLane(BaseModelTrackDateImpl):
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                                related_name="board_swim_lanes", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_swim_lanes")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
