
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_activity.models_activity import *
from app_common.mod_common.models_common import *

class Step(BaseModelImpl):
    activity = models.ForeignKey('app_organization.Activity', on_delete=models.CASCADE, 
                            related_name="activity_steps", null=True, blank=True)
    
    persona = models.ForeignKey('app_organization.Persona', on_delete=models.CASCADE,
                                related_name="persona_steps", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_steps")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
