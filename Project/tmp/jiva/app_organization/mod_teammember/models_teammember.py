
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_team.models_team import *
from app_common.mod_common.models_common import *

class Teammember(BaseModelTrackImpl):
    tea = models.ForeignKey('app_organization.Team', on_delete=models.CASCADE, 
                            related_name="tea_teammembers", null=True, blank=True)
    
    member = models.ForeignKey('app_memberprofilerole.Member', on_delete=models.CASCADE, 
                               null=True, blank=True) 
    
    member_role = models.ForeignKey('memberrole', on_delete=models.CASCADE, 
                               null=True, blank=True) 
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_teammembers")
   
        
    def __str__(self):
        return self.tea.name
