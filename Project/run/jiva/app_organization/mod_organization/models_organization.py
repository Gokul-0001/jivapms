
from app_organization.mod_app.all_model_imports import *
from app_common.mod_common.models_common import *

class Organization(BaseModelImpl):
    #org = models.ForeignKey('', on_delete=models.CASCADE, related_name="org_")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_Organization")
   
        
    def __str__(self):
        return self.name


class Siteorgrole(BaseModelTrackImpl):
    # This is for Organizations
    # SiteAdmin can view, admin all organizations
    # While OrgAdmin can view, admin only their organization where they have privileges
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Editor', 'Editor'),
        ('Viewer', 'Viewer'),
        ('NoView', 'No View'),
        # Add more roles as needed
    ]
    role_type = models.CharField(max_length=255, choices=ROLE_CHOICES, default='NoView')
    description = models.TextField(null=True, blank=True)
    
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_site_roles")
    
    def __str__(self):
        return self.get_role_type_display()


class Sitemembership(BaseModelTrackImpl):
    member = models.ForeignKey('app_memberprofilerole.Member', on_delete=models.CASCADE, related_name='site_memberships', null=True, blank=True)
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, related_name='site_orgs', null=True, blank=True)
    org_role = models.ForeignKey('Siteorgrole', on_delete=models.CASCADE, null=True, blank=True)  # Role in the project (e.g., 'Project Admin', 'Viewer')
    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_sitemembership")
    def __str__(self):
        return f"{self.member.user.username} in {self.org.name} "



