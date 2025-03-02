
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project_workflow.models_project_workflow import *
from app_common.mod_common.models_common import *

class ProjectWorkflowStep(BaseModelImpl):
    project_workflow = models.ForeignKey('app_organization.ProjectWorkflow', on_delete=models.CASCADE, 
                            related_name="project_workflow_project_workflow_steps", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_workflow_steps")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
