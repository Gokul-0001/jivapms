
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_impact_mapping.models_impact_mapping import *

class ImpactMappingForm(forms.ModelForm):
    class Meta:
        model = ImpactMapping
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ImpactMappingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

