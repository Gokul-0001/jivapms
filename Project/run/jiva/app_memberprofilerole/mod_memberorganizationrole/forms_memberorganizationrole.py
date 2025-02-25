

from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_member.models_member import *

class MemberorganizationroleForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = MemberOrganizationRole
        fields = ['member', 'org', 'role']  # Keep original fields

    def __init__(self, *args, **kwargs):
        super(MemberorganizationroleForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.member and self.instance.member.user:
            self.fields['first_name'].initial = self.instance.member.user.first_name
            self.fields['last_name'].initial = self.instance.member.user.last_name
            self.fields['email'].initial = self.instance.member.user.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Update the User model fields
        if instance.member and instance.member.user:
            user = instance.member.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            
            if commit:
                user.save()  # Save user changes
                instance.save()  # Save MemberOrganizationRole changes

        return instance
