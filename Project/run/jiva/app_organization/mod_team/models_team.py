
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Team(BaseModelImpl):
    org = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="org_teams", null=True, blank=True)
    
    members = models.ManyToManyField('app_memberprofilerole.Member', related_name='teams')
    projects = models.ManyToManyField('app_organization.Project', related_name='teams')
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_teams")
   
        
    def __str__(self):
        return self.name


############################################################################################################

"""
team = Team.objects.get(id=team_id)
projects = team.projects.all()  # This will give you all projects associated with the team

project = Project.objects.get(id=project_id)
teams = project.teams.all()  # This will give you all teams associated with the project

"""