
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_practice_event.models_org_practice_event import *

class OrgPracticeEventForm(forms.ModelForm):
    class Meta:
        model = OrgPracticeEvent
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OrgPracticeEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

