
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_team.models_org_team import *

class OrgTeamForm(forms.ModelForm):
    class Meta:
        model = OrgTeam
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(OrgTeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

