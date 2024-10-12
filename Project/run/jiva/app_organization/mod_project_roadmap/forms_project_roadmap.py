
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_roadmap.models_project_roadmap import *

class ProjectRoadmapForm(forms.ModelForm):
    class Meta:
        model = ProjectRoadmap
        fields = ['section', 'task_name', 'status', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(ProjectRoadmapForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

