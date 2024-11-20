
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class OpsValueStream(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_ops_value_streams", null=True, blank=True)
    
    trigger = models.CharField(max_length=150, null=True, blank=True)
    value = models.CharField(max_length=150, null=True, blank=True)
    
    # add all the calculated fields here    
    total_time = models.PositiveIntegerField(default=0)
    value_time = models.PositiveIntegerField(default=0)
    delay_time = models.PositiveIntegerField(default=0)
    efficiency = models.FloatField(default=0)
    rolled_percentage_avg = models.FloatField(default=0)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_ops_value_streams")
   
        
    def __str__(self):
        return self.name
