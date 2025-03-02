
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_workflow.models_project_workflow import *

class ProjectWorkflowForm(forms.ModelForm):
    class Meta:
        model = ProjectWorkflow
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectWorkflowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

