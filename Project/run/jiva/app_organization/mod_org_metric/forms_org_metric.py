
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_metric.models_org_metric import *

class OrgMetricForm(forms.ModelForm):
    class Meta:
        model = OrgMetric
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OrgMetricForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

