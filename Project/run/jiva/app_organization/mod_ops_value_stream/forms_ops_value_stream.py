
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_ops_value_stream.models_ops_value_stream import *

class OpsValueStreamForm(forms.ModelForm):
    class Meta:
        model = OpsValueStream
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OpsValueStreamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

