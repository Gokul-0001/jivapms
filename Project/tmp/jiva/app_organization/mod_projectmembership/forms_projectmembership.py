
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *

class ProjectmembershipForm(forms.ModelForm):
    class Meta:
        model = Projectmembership
        fields = ['member', 'project', 'project_role', 'team']
    def __init__(self, *args, **kwargs):
        super(ProjectmembershipForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

