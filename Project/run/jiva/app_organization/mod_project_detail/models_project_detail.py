
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *

class ProjectDetail(BaseModelTrackImpl):
    pro = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="project_details", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_details")
   
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name='org_project_details', null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    values = models.TextField(null=True, blank=True)
    strategy = models.TextField(null=True, blank=True)
    roadmap_description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.pro.name
    
