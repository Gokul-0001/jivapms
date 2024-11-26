
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_work_flow.models_org_work_flow import *

class OrgWorkFlowForm(forms.ModelForm):
    class Meta:
        model = OrgWorkFlow
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OrgWorkFlowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

