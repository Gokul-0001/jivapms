
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_project_board_swimlane.models_project_board_swimlane import *
from app_organization.mod_org_board.models_org_board import *
class ProjectBoardSwimlaneForm(forms.ModelForm):
    class Meta:
        model = ProjectBoardSwimLane
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectBoardSwimlaneForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

