
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_organization.mod_project_template.models_project_template import *
class OrgEvent(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_org_events", null=True, blank=True)
    
    project_template = models.ForeignKey('app_organization.ProjectTemplate', on_delete=models.SET_NULL, 
                                         related_name="project_template_org_events", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_events")
   
        
    def __str__(self):
        return self.name
