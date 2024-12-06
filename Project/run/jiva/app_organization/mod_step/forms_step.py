
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_step.models_step import *

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

