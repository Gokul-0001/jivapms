
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_workflow_step.models_project_workflow_step import *

class ProjectWorkflowStepForm(forms.ModelForm):
    class Meta:
        model = ProjectWorkflowStep
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectWorkflowStepForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

