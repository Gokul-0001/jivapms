
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_org_release.models_org_release import *
from app_common.mod_common.models_common import *

from app_common.mod_app.all_view_imports import *

class OrgIteration(BaseModelTrackDateImpl):
    org_release = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, 
                            related_name="org_release_org_iterations", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE,
                                related_name="project_org_iterations", null=True, blank=True)
    
    iteration_length = models.PositiveIntegerField(default=2)
    
    quarter = models.PositiveIntegerField(default=1)
    iteration_number = models.PositiveIntegerField(default=0)
    
    iteration_start_date = models.DateTimeField(null=True, blank=True)
    iteration_end_date = models.DateTimeField(null=True, blank=True)
    
    start_day = models.CharField(max_length=15, null=True, blank=True)
    end_day = models.CharField(max_length=15, null=True, blank=True)
    
   
    version = models.CharField(max_length=50, null=True, blank=True)
    build_no = models.CharField(max_length=50, null=True, blank=True)
    hotfix = models.CharField(max_length=50, null=True, blank=True)
    
    
    timestamp = models.DateTimeField(null=True, blank=True)

    
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_iterations")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
        
    # Store date only (time set to 00:00:00)
    def set_date_only(self, date_value):
        if isinstance(date_value, datetime):
            date_value = date_value.date()
        self.timestamp = datetime.combine(date_value, datetime.min.time())
        self.save()

    # Store date and time
    def set_date_and_time(self, date_time_value):
        if isinstance(date_time_value, datetime):
            self.timestamp = date_time_value
        else:
            raise ValueError("Input should be a datetime object")
        self.save()

    # Retrieve date only
    def get_date_only(self):
        return self.timestamp.date()

    # Retrieve date and time
    def get_date_and_time(self):
        return self.timestamp


class ProjectIteration(BaseModelTrackDateImpl):
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE,
                                related_name="project_iterations", null=True, blank=True)
    
    # store all the project iterations data
    iteration_goal = models.TextField(null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_org_project_iterations")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)

