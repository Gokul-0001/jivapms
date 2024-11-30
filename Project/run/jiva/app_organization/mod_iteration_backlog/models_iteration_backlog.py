
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_iteration.models_iteration import *
from app_common.mod_common.models_common import *

class IterationBacklog(BaseModelImpl):
    backlog_item = TreeForeignKey("app_organization.Backlog", null=True, blank=True, 
                          related_name='backlog_items', 
                          on_delete=models.CASCADE)
    iteration = models.ForeignKey('app_organization.Iteration', on_delete=models.CASCADE, 
                            related_name="iteration_iteration_backlogs", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_iteration_backlogs")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
