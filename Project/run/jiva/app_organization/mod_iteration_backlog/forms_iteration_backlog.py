
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_iteration_backlog.models_iteration_backlog import *

class IterationBacklogForm(forms.ModelForm):
    class Meta:
        model = IterationBacklog
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(IterationBacklogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

