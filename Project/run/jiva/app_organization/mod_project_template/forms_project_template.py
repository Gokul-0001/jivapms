
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_template.models_project_template import *

class ProjectTemplateForm(forms.ModelForm):
    class Meta:
        model = ProjectTemplate
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectTemplateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

