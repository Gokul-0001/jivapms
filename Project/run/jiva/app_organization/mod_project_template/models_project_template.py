
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class ProjectTemplate(BaseModelTrackImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_project_templates", null=True, blank=True)
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE,
                                null=True, blank=True,
                                related_name="project_templates")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_templates")
    
    # like Scrum, Kanban, Waterfall, etc.
    name = models.CharField(max_length=200, null=True, blank=True)
    # Description of the template
    description = models.TextField(null=True, blank=True)
    
    
        
    def __str__(self):
        return self.name
