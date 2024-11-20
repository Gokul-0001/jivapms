
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_release.models_release import *

class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

