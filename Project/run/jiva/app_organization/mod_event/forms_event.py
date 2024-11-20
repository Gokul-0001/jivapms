
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_event.models_event import *

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

