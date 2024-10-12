
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_detail.models_project_detail import *

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = ['vision', 'mission', 'values', 'strategy', 'roadmap_description']
    def __init__(self, *args, **kwargs):
        super(ProjectDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

