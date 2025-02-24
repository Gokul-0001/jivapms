from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_organization.models_organization import *
User = get_user_model()

class Command(BaseCommand):
    help = "Manage organization users, members, and soft delete organizations."

    def add_arguments(self, parser):
        parser.add_argument(
            'org_id_or_action', type=str,
            help="Use 'list-organizations' or provide an organization ID."
        )
        parser.add_argument(
            'action', type=str, nargs='?',
            choices=['list-users', 'delete-users', 'delete-members', 'delete-member-users', 'delete-organization'],
            help="Action to perform: list-users, delete-users, delete-members, delete-member-users, delete-organization (only required if org_id is given)."
        )

    def handle(self, *args, **options):
        org_id_or_action = options['org_id_or_action']
        action = options['action']

        if org_id_or_action == "list-organizations":
            self.list_organizations()
        elif org_id_or_action == "list-deleted-organizations":
            self.list_deleted_organizations()
        elif org_id_or_action.isdigit():
            org_id = int(org_id_or_action)
            if not Organization.objects.filter(id=org_id).exists():
                self.stderr.write(self.style.ERROR(f"Organization with ID {org_id} does not exist."))
                return
            if action == "list-users":
                self.list_users(org_id)
            elif action == "delete-users":
                self.soft_delete_users(org_id)
            elif action == "delete-members":
                self.soft_delete_members(org_id)
            elif action == "delete-member-users":
                self.soft_delete_users(org_id)
                self.soft_delete_members(org_id)
            elif action == "delete-organization":
                self.soft_delete_organization(org_id)
            else:
                self.stderr.write(self.style.ERROR("Invalid action. Use list-users, delete-users, delete-members, delete-member-users, or delete-organization."))
        else:
            self.stderr.write(self.style.ERROR("Invalid argument. Use 'list-organizations' or an organization ID."))

    def list_organizations(self):
        """List all organizations"""
        organizations = Organization.objects.filter(active=True)
        if not organizations:
            self.stdout.write(self.style.WARNING("No organizations found."))
        else:
            self.stdout.write(self.style.SUCCESS("List of Organizations:"))
            for org in organizations:
                self.stdout.write(f"ID: {org.id} | Name: {org.name}")

    def list_deleted_organizations(self):
        """List deleted organizations"""
        organizations = Organization.objects.filter(active=False)
        if not organizations:
            self.stdout.write(self.style.WARNING("No organizations found."))
        else:
            self.stdout.write(self.style.SUCCESS("List of Deleted Organizations:"))
            for org in organizations:
                self.stdout.write(f"ID: {org.id} | Name: {org.name}")

    def list_users(self, org_id):
        """List users in a specific organization via MemberOrganizationRole"""
        roles = MemberOrganizationRole.objects.filter(org_id=org_id).select_related('member__user')

        if not roles.exists():
            self.stdout.write(self.style.WARNING(f"No users/members found for organization ID {org_id}."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Users and Members in Organization {org_id}:"))
            for role in roles:
                member = role.member
                if member and member.user:
                    self.stdout.write(f"User ID: {member.user.id} | Username: {member.user.username} | Email: {member.user.email}")
                self.stdout.write(f"Member ID: {member.id} | Organization: {role.org.name} | Role: {role.role.name}")

    def soft_delete_users(self, org_id):
        """Soft delete users (set is_active=False) based on MemberOrganizationRole"""
        roles = MemberOrganizationRole.objects.filter(org_id=org_id).select_related('member__user')

        users = {role.member.user for role in roles if role.member and role.member.user and role.member.user.is_active}

        if not users:
            self.stdout.write(self.style.WARNING(f"No active users found for organization ID {org_id}."))
        else:
            user_ids = [user.id for user in users]
            count = User.objects.filter(id__in=user_ids).update(is_active=False)
            self.stdout.write(self.style.SUCCESS(f"Soft deleted {count} users in organization ID {org_id}."))

    def soft_delete_members(self, org_id):
        """Soft delete members (set active=False, deleted=True) based on MemberOrganizationRole"""
        roles = MemberOrganizationRole.objects.filter(org_id=org_id).select_related('member')

        members = {role.member for role in roles if role.member and role.member.active}

        if not members:
            self.stdout.write(self.style.WARNING(f"No active members found for organization ID {org_id}."))
        else:
            member_ids = [member.id for member in members]
            count = Member.objects.filter(id__in=member_ids).update(active=False, deleted=True)
            self.stdout.write(self.style.SUCCESS(f"Soft deleted {count} members in organization ID {org_id}."))

    def soft_delete_organization(self, org_id):
        """Soft delete the organization (set active=False, deleted=True)"""
        org = Organization.objects.filter(id=org_id, active=True).first()

        if not org:
            self.stdout.write(self.style.WARNING(f"No active organization found for ID {org_id}."))
        else:
            org.active = False
            org.deleted = True
            org.save()
            self.stdout.write(self.style.SUCCESS(f"Soft deleted Organization ID {org_id} - {org.name}."))
