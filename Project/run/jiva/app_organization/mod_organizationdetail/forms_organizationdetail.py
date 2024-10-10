
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_organizationdetail.models_organizationdetail import *

class OrganizationdetailForm(forms.ModelForm):
    class Meta:
        model = Organizationdetail
        fields = ['org', 'vision', 'mission', 'values', 'strategy', 'roadmap_description']
    def __init__(self, *args, **kwargs):
        super(OrganizationdetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

