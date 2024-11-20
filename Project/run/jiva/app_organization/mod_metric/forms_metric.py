
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_metric.models_metric import *

class MetricForm(forms.ModelForm):
    class Meta:
        model = Metric
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(MetricForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

