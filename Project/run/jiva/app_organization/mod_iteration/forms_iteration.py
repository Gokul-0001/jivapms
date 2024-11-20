
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_iteration.models_iteration import *

class IterationForm(forms.ModelForm):
    class Meta:
        model = Iteration
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(IterationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

