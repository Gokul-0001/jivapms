
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_framework.models_framework import *

class FrameworkForm(forms.ModelForm):
    class Meta:
        model = Framework
        fields = ['name', 'description', 'content', 'default_text']
    def __init__(self, *args, **kwargs):
        super(FrameworkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

