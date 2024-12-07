from django.core.management.base import BaseCommand
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_step.models_step import *


class Command(BaseCommand):
    help = 'Load test data for Persona, Activities, and Steps'

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid duplicates
        Step.objects.all().delete()
        Activity.objects.all().delete()
        Persona.objects.all().delete()

        # Create a Persona
        persona = Persona.objects.create(
            name="John Doe / Project Manager",
            description="John is a project manager responsible for overseeing software development projects.",
            organization_id=1,
        )
        self.stdout.write(f"Created Persona: {persona.name}")

        # Define activities and steps
        activities = [
            {
                "name": "Plan Project",
                "description": "Activities related to planning a new project.",
                "steps": [
                    {"name": "Define objectives", "description": "Identify the key objectives of the project."},
                    {"name": "Create timeline", "description": "Draft a realistic project timeline."},
                    {"name": "Allocate resources", "description": "Assign team members and other resources to tasks."},
                ],
            },
            {
                "name": "Conduct Meetings",
                "description": "Activities related to conducting team meetings.",
                "steps": [
                    {"name": "Schedule meetings", "description": "Plan and schedule meetings with stakeholders."},
                    {"name": "Prepare agenda", "description": "Draft the agenda for the meeting."},
                    {"name": "Document minutes", "description": "Record the key points and decisions from the meeting."},
                ],
            },
            {
                "name": "Monitor Progress",
                "description": "Activities related to monitoring project progress.",
                "steps": [
                    {"name": "Track milestones", "description": "Monitor the completion of project milestones."},
                    {"name": "Update stakeholders", "description": "Provide regular updates to stakeholders."},
                    {"name": "Identify risks", "description": "Identify and mitigate project risks."},
                ],
            },
            {
                "name": "Manage Team",
                "description": "Activities related to managing the project team.",
                "steps": [
                    {"name": "Conduct 1-on-1s", "description": "Hold one-on-one meetings with team members."},
                    {"name": "Provide feedback", "description": "Offer constructive feedback to the team."},
                    {"name": "Resolve conflicts", "description": "Address and resolve conflicts within the team."},
                ],
            },
            {
                "name": "Deliver Project",
                "description": "Activities related to delivering the project.",
                "steps": [
                    {"name": "Conduct testing", "description": "Ensure all deliverables are tested thoroughly."},
                    {"name": "Prepare documentation", "description": "Prepare project documentation for handover."},
                    {"name": "Close project", "description": "Complete the project and review outcomes."},
                ],
            },
        ]

        # Create Activities and Steps
        for activity_data in activities:
            activity = Activity.objects.create(
                persona=persona,
                name=activity_data["name"],
                description=activity_data["description"],
            )
            self.stdout.write(f"  Created Activity: {activity.name}")

            for step_data in activity_data["steps"]:
                step = Step.objects.create(
                    activity=activity,
                    name=step_data["name"],
                    description=step_data["description"],
                )
                self.stdout.write(f"    Created Step: {step.name}")

        self.stdout.write(self.style.SUCCESS("Test data loaded successfully!"))
