
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_ops_value_stream_step.models_ops_value_stream_step import *

class OpsValueStreamStepForm(forms.ModelForm):
    class Meta:
        model = OpsValueStreamStep
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OpsValueStreamStepForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

