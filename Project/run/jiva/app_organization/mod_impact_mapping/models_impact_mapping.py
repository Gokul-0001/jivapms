
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class ImpactMapping(BaseModelImpl):
    organization = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="organization_impact_mappings", null=True, blank=True)
    
    impact_map = models.OneToOneField(
        'app_organization.ImpactMap',
        on_delete=models.CASCADE,
        related_name='impact_map',
        null=True,
        blank=True
    )
   
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_impact_mappings")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)



class ImpactMap(BaseModelTrackDateImpl, MPTTModel):
    
    NODE_TYPES = (
        ('Goal', 'Goal'),
        ('Actor', 'Actor'),
        ('Impact', 'Impact'),
        ('Deliverable', 'Deliverable'),
        ('Task', 'Task'),
    )
    

    node_type = models.CharField(max_length=20, choices=NODE_TYPES, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

   
        
    def get_children(self):
        return self.children.filter(active=True).order_by('position')

    def __str__(self):
        return f"{self.node_type}: {self.name}"