
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *


class Projectmembership(BaseModelTrackImpl):
    member = models.ForeignKey('app_memberprofilerole.Member', on_delete=models.CASCADE, related_name='project_memberships', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_members', null=True, blank=True)
    project_role = models.ForeignKey('ProjectRole', on_delete=models.CASCADE, null=True, blank=True)  # Role in the project (e.g., 'Project Admin', 'Viewer')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_projectmembership")
    def __str__(self):
        return f"{self.member.user.username} in {self.project.name} "
