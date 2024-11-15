
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_dev_value_stream_step.models_dev_value_stream_step import *

class DevValueStreamStepForm(forms.ModelForm):
    class Meta:
        model = DevValueStreamStep
        fields = ['name', 'description', 'value', 'delay']
    def __init__(self, *args, **kwargs):
        super(DevValueStreamStepForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

