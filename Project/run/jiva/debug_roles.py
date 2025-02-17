import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_mgr.settings')
django.setup()

# Now you can safely import your models
from django.contrib.auth.models import User
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_project.models_project import *
from app_memberprofilerole.mod_role.models_role import *

def check_member_role():
    user = User.objects.filter(username='david.miller').first()
    
    organization = Organization.objects.filter(name='TEST1 Org').first()
    mem1 = Member.objects.filter(user=user, org_id=organization.id).first()
    print(f">>> === Member ID: {mem1.id} === <<<")
    role = Role.objects.get(name='Org Admin')  # Assuming the role name is correct

    try:
        member = Member.objects.get(user=user, org=organization)
        org_membership = MemberOrganizationRole.objects.get(member=member, org=organization, role=role)
        print(f"Member ID: {member.id}, Role: {org_membership.role.name}")
    except User.DoesNotExist:
        print("User not found.")
    except Organization.DoesNotExist:
        print("Organization not found.")
    except Role.DoesNotExist:
        print("Role not found.")
    except Member.DoesNotExist:
        print("Member not found.")
    except MemberOrganizationRole.DoesNotExist:
        print("Membership or role in organization not found.")

if __name__ == "__main__":
    check_member_role()
