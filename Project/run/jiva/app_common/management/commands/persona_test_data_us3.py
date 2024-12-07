from django.core.management.base import BaseCommand
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_step.models_step import *
from app_organization.mod_backlog.models_backlog import *

import random

class Command(BaseCommand):
    help = 'Load test data for Persona, Activities, Steps, and User Stories'

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid duplicates
        #UserStory.objects.all().delete()
        # Step.objects.all().delete()
        # Activity.objects.all().delete()
        # Persona.objects.all().delete()

        # Create a Persona
        persona = Persona.objects.create(
            name="Sarah Smith / Product Manager Persona",
            description="Sarah is a product manager responsible for overseeing product's success.",
            organization_id=1,
        )
        self.stdout.write(f"Created Persona: {persona.name}")

        # Define activities, steps, and user stories
        activities = [
            {
                "name": "Plan Project",
                "description": "Activities related to planning a new project.",
                "steps": [
                    {
                        "name": "Define objectives",
                        "description": "Identify the key objectives of the project.",
                        "user_stories": [
                            {"name": "Define project goals", "description": "As a project manager, I want to identify project goals to align the team toward a common purpose."},
                            {"name": "Document deliverables", "description": "As a project manager, I want to document key deliverables so stakeholders have clear expectations."}
                        ]
                    },
                    {
                        "name": "Create timeline",
                        "description": "Draft a realistic project timeline.",
                        "user_stories": [
                            {"name": "Set project phases", "description": "As a project manager, I want to define the project phases and timelines so that the team can plan effectively."},
                            {"name": "Add buffer time", "description": "As a project manager, I want to include buffer time in the timeline to mitigate potential delays."},
                            {"name": "Communicate timeline", "description": "As a project manager, I want to share the timeline with stakeholders to set clear expectations."}
                        ]
                    },
                    {
                        "name": "Allocate resources",
                        "description": "Assign team members and other resources to tasks.",
                        "user_stories": [
                            {"name": "Assign tasks efficiently", "description": "As a project manager, I want to assign tasks based on expertise to ensure efficiency."},
                            {"name": "Track resource availability", "description": "As a project manager, I want to track resource availability to avoid overloading team members."}
                        ]
                    }
                ]
            },
            {
                "name": "Conduct Meetings",
                "description": "Activities related to conducting team meetings.",
                "steps": [
                    {
                        "name": "Schedule meetings",
                        "description": "Plan and schedule meetings with stakeholders.",
                        "user_stories": [
                            {"name": "Plan weekly stand-ups", "description": "As a project manager, I want to schedule weekly stand-ups to keep the team updated on progress."},
                            {"name": "Set convenient times", "description": "As a project manager, I want to set meeting times that accommodate all stakeholders to maximize participation."}
                        ]
                    },
                    {
                        "name": "Prepare agenda",
                        "description": "Draft the agenda for the meeting.",
                        "user_stories": [
                            {"name": "Create focused agenda", "description": "As a project manager, I want to create a clear meeting agenda to keep discussions focused."},
                            {"name": "Prioritize topics", "description": "As a project manager, I want to prioritize critical topics in the agenda to address urgent issues first."}
                        ]
                    },
                    {
                        "name": "Document minutes",
                        "description": "Record the key points and decisions from the meeting.",
                        "user_stories": [
                            {"name": "Capture key decisions", "description": "As a project manager, I want to record key decisions made during meetings to ensure shared understanding."},
                            {"name": "List action items", "description": "As a project manager, I want to capture action items to ensure follow-up tasks are completed."}
                        ]
                    }
                ]
            },
            {
                "name": "Monitor Progress",
                "description": "Activities related to monitoring project progress.",
                "steps": [
                    {
                        "name": "Track milestones",
                        "description": "Monitor the completion of project milestones.",
                        "user_stories": [
                            {"name": "Track milestone status", "description": "As a project manager, I want to track milestones to assess if the project is on schedule."},
                            {"name": "Identify milestone delays", "description": "As a project manager, I want to identify delays in milestones to adjust the timeline as needed."}
                        ]
                    },
                    {
                        "name": "Update stakeholders",
                        "description": "Provide regular updates to stakeholders.",
                        "user_stories": [
                            {"name": "Share weekly updates", "description": "As a project manager, I want to provide weekly updates to stakeholders to ensure transparency."},
                            {"name": "Highlight risks", "description": "As a project manager, I want to share risks and mitigation plans with stakeholders to maintain trust."}
                        ]
                    },
                    {
                        "name": "Identify risks",
                        "description": "Identify and mitigate project risks.",
                        "user_stories": [
                            {"name": "Spot early risks", "description": "As a project manager, I want to identify potential risks early to minimize their impact."},
                            {"name": "Document mitigation plans", "description": "As a project manager, I want to document mitigation plans for critical risks to avoid delays."}
                        ]
                    }
                ]
            },
            {
                "name": "Manage Team",
                "description": "Activities related to managing the project team.",
                "steps": [
                    {
                        "name": "Conduct 1-on-1s",
                        "description": "Hold one-on-one meetings with team members.",
                        "user_stories": [
                            {"name": "Discuss progress", "description": "As a project manager, I want to hold 1-on-1 meetings to address individual progress and concerns."},
                            {"name": "Set personal goals", "description": "As a project manager, I want to set personal development goals with team members to support their growth."}
                        ]
                    },
                    {
                        "name": "Provide feedback",
                        "description": "Offer constructive feedback to the team.",
                        "user_stories": [
                            {"name": "Offer actionable feedback", "description": "As a project manager, I want to provide actionable feedback to help team members improve performance."},
                            {"name": "Acknowledge achievements", "description": "As a project manager, I want to recognize team members' achievements to boost morale."}
                        ]
                    },
                    {
                        "name": "Resolve conflicts",
                        "description": "Address and resolve conflicts within the team.",
                        "user_stories": [
                            {"name": "Mediate team conflicts", "description": "As a project manager, I want to mediate conflicts between team members to maintain a healthy work environment."},
                            {"name": "Document conflict resolution", "description": "As a project manager, I want to document conflict resolutions to prevent future misunderstandings."}
                        ]
                    }
                ]
            },
            {
                "name": "Deliver Project",
                "description": "Activities related to delivering the project.",
                "steps": [
                    {
                        "name": "Conduct testing",
                        "description": "Ensure all deliverables are tested thoroughly.",
                        "user_stories": [
                            {"name": "Ensure feature testing", "description": "As a project manager, I want to ensure all features are tested before release to maintain quality."},
                            {"name": "Prioritize critical tests", "description": "As a project manager, I want to prioritize critical tests to meet the release deadline."}
                        ]
                    },
                    {
                        "name": "Prepare documentation",
                        "description": "Prepare project documentation for handover.",
                        "user_stories": [
                            {"name": "Prepare user manuals", "description": "As a project manager, I want to prepare user manuals to support end users after release."},
                            {"name": "Document lessons learned", "description": "As a project manager, I want to document lessons learned to improve future projects."}
                        ]
                    },
                    {
                        "name": "Close project",
                        "description": "Complete the project and review outcomes.",
                        "user_stories": [
                            {"name": "Review project success", "description": "As a project manager, I want to conduct a final review with stakeholders to evaluate project success."},
                            {"name": "Archive project docs", "description": "As a project manager, I want to archive project documents for future reference."}
                        ]
                    }
                ]
            }
        ]

        # Create Activities, Steps, and User Stories
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

                 
                for user_story_data in step_data["user_stories"]:
                    story = Backlog.objects.create(
                        pro_id=10,
                        type_id=17,
                        parent_id=15,
                        name=user_story_data["name"],
\
                    )
                    self.stdout.write(f"      Created User Story: {story.name}")


        self.stdout.write(self.style.SUCCESS("Test data loaded successfully!"))
