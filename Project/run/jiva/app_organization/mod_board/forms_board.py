
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_board.models_board import *

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

