
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *

class Release(BaseModelTrackDateImpl):
    pro = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="pro_releases", null=True, blank=True)
    
    release_length = models.PositiveIntegerField(default=3)
    
    apply_release_iteration_length = models.PositiveIntegerField(default=2)
    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_releases")
   
        
    def __str__(self):
        return self.name
