
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Organizationdetail(BaseModelTrackImpl):
    org = models.ForeignKey('Organization', on_delete=models.CASCADE, 
                            related_name='org_details', null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    values = models.TextField(null=True, blank=True)
    strategy = models.TextField(null=True, blank=True)
    roadmap_description = models.TextField(blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_organizationdetail")

    def __str__(self):
        return self.org.name
    