
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_board_state.models_project_board_state import *
from app_organization.mod_org_board.models_org_board import *
class ProjectBoardStateForm(forms.ModelForm):
    class Meta:
        model = ProjectBoardState
        fields = ['name', 'description', 'buffer_column']
    def __init__(self, *args, **kwargs):
        super(ProjectBoardStateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

