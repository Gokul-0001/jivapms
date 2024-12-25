
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_event.models_org_event import *

class OrgEventForm(forms.ModelForm):
    class Meta:
        model = OrgEvent
        fields = ['name', 'description', 'project_template']
    def __init__(self, *args, **kwargs):
        super(OrgEventForm, self).__init__(*args, **kwargs)
        
        self.fields['project_template'].queryset = ProjectTemplate.objects.filter(active=True)
        
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

