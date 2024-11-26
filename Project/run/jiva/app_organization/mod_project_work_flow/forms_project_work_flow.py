
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_work_flow.models_project_work_flow import *

class ProjectWorkFlowForm(forms.ModelForm):
    class Meta:
        model = ProjectWorkFlow
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectWorkFlowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

