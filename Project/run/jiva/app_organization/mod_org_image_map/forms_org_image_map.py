
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.mod_framework.models_framework import *
from app_jivapms.mod_app.all_view_imports import *
class OrgImageMapForm(forms.ModelForm):
    supporting_frameworks = forms.ModelMultipleChoiceField(
        queryset=Framework.objects.none(),  # Placeholder queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = OrgImageMap
        fields = ['name', 'description', 'image', 'display_flag', 'supporting_frameworks' ]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        org_id = kwargs.pop('org_id', None)  # Assuming org_id is passed to the form
        super(OrgImageMapForm, self).__init__(*args, **kwargs)
        
        # Custom widget for the image field
        if self.instance and self.instance.image:
            self.fields['image'].widget = forms.ClearableFileInput(attrs={
                'accept': 'image/*',  # Allows only images
                'style': 'max-width:100%; height:auto;',  # Prevents thumbnail constraint
            })
        
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False
        
        organization = get_object_or_404(Organization, pk=org_id, active=True)
        if org_id:
            self.fields['supporting_frameworks'].queryset = Framework.objects.filter(
                organization=organization,
                active=True,
            )
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("An image file is required.")
        return image
    