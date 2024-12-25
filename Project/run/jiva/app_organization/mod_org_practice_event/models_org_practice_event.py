
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_org_event.models_org_event import *
from app_common.mod_common.models_common import *

class OrgPracticeEvent(BaseModelTrackDateImpl):
    org_event = models.ForeignKey('app_organization.OrgEvent', on_delete=models.CASCADE, 
                            related_name="org_event_org_practice_events", null=True, blank=True)
    
    
    purpose = models.TextField(null=True, blank=True)
    event_facilitation = models.TextField(null=True, blank=True)
    event_duration = models.FloatField(null=True, blank=True)
    event_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name="event_owner_org_practice_events")
    
    
    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_practice_events")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
