
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_board.models_project_board import *
from app_organization.mod_org_board.models_org_board import *
class ProjectBoardForm(forms.ModelForm):
    class Meta:
        model = ProjectBoard
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectBoardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

