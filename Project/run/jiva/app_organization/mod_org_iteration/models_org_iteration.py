
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_org_release.models_org_release import *
from app_common.mod_common.models_common import *

class OrgIteration(BaseModelTrackDateImpl):
    rel = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, 
                            related_name="org_rel_iterations", null=True, blank=True)
    
    iteration_length = models.PositiveIntegerField(default=2)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_iterations")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
