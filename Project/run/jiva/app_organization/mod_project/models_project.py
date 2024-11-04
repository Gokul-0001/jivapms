
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

from app_organization.mod_team.models_team import *

class Project(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_projects", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_projects")
   
        
    def __str__(self):
        return self.name


class ProjectRole(BaseModelTrackImpl):
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
                               related_name="author_project_roles")
    
    def __str__(self):
        return self.get_role_type_display()

# this will be used for administration of the project
# will tell the state and other important decisions of the project
class ProjectAdministration(BaseModelTrackImpl):
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name="project_administrations")
    
    PROJECT_STATE_CHOICES = [
        ('Initiation', 'Initiation'),
        ('Started', 'Started'),
        ('Launched', 'Launched'),
        ('Archived', 'Archived'),
        # Add more states as needed
    ]
    project_state = models.CharField(max_length=255, choices=PROJECT_STATE_CHOICES, 
                                 default='Initiation')
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_project_administrations")
    
    def __str__(self):
        return self.project.name





"""
==================================================================
Example Permissions Breakdown:
Organization Admin:
Can create and manage projects.
Can manage all members and roles within the organization.

Project Admin:
Can manage the specific project, assign roles, and edit project details.

Editor:
Can edit content within the project but has no permission to manage users or roles.

Viewer:
Can only view project content.
"""