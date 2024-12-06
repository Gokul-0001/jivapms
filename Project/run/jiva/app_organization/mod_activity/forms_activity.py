
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_activity.models_activity import *

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

