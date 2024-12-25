
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class OrgRelease(BaseModelTrackDateImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_org_releases", null=True, blank=True)
    
    release_length = models.PositiveIntegerField(default=3)
    
    planning_buffer = models.PositiveIntegerField(default=2)
    
    apply_release_iteration_length = models.PositiveIntegerField(default=2)
    
    # 23/12/2024 for roadmapping
    no_of_iterations = models.IntegerField(default=5)
    # New Predecessor Field (Multiple Dependencies)
    predecessors = models.ManyToManyField('self', blank=True, related_name="successors")
    
    quarter = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    release_official_name = models.CharField(max_length=150, null=True, blank=True)
    release_start_date = models.DateField(null=True, blank=True)
    release_end_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    major_version = models.CharField(max_length=50, null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_releases")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
