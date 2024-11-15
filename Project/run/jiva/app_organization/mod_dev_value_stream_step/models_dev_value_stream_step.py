
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_dev_value_stream.models_dev_value_stream import *
from app_common.mod_common.models_common import *

class DevValueStreamStep(BaseModelImpl):
    value = models.PositiveIntegerField(default=0)
    delay = models.PositiveIntegerField(default=0)
    dev = models.ForeignKey('app_organization.DevValueStream', on_delete=models.CASCADE, 
                            related_name="dev_dev_value_stream_steps", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_dev_value_stream_steps")
    
        
    def __str__(self):
        return self.name
