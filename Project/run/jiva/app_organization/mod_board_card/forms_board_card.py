
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_board_card.models_board_card import *

class BoardCardForm(forms.ModelForm):
    class Meta:
        model = BoardCard
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(BoardCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

