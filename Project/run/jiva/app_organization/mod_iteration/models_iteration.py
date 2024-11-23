
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_release.models_release import *
from app_common.mod_common.models_common import *

class Iteration(BaseModelImpl):
    rel = models.ForeignKey('app_organization.Release', on_delete=models.CASCADE, 
                            related_name="rel_iterations", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_iterations")
    

        
    def __str__(self):
        return self.name
