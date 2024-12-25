
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_org_release.models_org_release import *
from app_common.mod_common.models_common import *

class OrgIteration(BaseModelTrackDateImpl):
    org_release = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, 
                            related_name="org_release_org_iterations", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE,
                                related_name="project_org_iterations", null=True, blank=True)
    
    iteration_length = models.PositiveIntegerField(default=2)
    
    quarter = models.PositiveIntegerField(default=1)
    iteration_number = models.PositiveIntegerField(default=0)
    
    iteration_start_date = models.DateField(null=True, blank=True)
    iteration_end_date = models.DateField(null=True, blank=True)
    
    start_day = models.CharField(max_length=15, null=True, blank=True)
    end_day = models.CharField(max_length=15, null=True, blank=True)
    
   
    version = models.CharField(max_length=50, null=True, blank=True)
    build_no = models.CharField(max_length=50, null=True, blank=True)
    hotfix = models.CharField(max_length=50, null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_iterations")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
