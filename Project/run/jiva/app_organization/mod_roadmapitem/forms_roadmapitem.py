
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_roadmapitem.models_roadmapitem import *

class RoadmapitemForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Enable HTML5 date picker
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Enable HTML5 date picker
    )
    class Meta:
        model = Roadmapitem
        fields = ['section', 'task_name', 'status', 'start_date', 'end_date']
    def __init__(self, *args, **kwargs):
        super(RoadmapitemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

