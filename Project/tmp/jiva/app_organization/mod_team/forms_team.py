
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_team.models_team import *

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

