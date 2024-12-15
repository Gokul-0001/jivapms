from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden
from functools import wraps
from django.db.models import *
from django.http import Http404
from django.utils.html import strip_tags
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template import Template, Context
from markdownx.utils import markdownify
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower, Trim
from itertools import chain
from markdownx.models import MarkdownxField
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Sum, FloatField
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from datetime import timedelta
from django.contrib.auth.models import Permission
from django.core.serializers.json import DjangoJSONEncoder
from collections import defaultdict
from django.template import Template, Context
from markdownx.utils import markdownify
from django.db import transaction
from collections import defaultdict
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from PIL import Image 
from lxml import etree
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.db import transaction
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.cache import cache


import traceback

import base64
import os
import platform
import json
import random
from django.http import JsonResponse
from django.apps import apps
from django.utils.timezone import make_aware
from datetime import datetime
import pytz


SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')

##################################  CONSTANTS ##################################

15/12/2024
# Flat backlog additions
FLAT_BACKLOG_ROOT_NAME = "Flat Backlog"



FLAT_BACKLOG_TYPES = {
    "Flat Backlog": "Flat Backlog",
    "USER STORY": "User Story",
    "TASK": "Task",
    "BUG": "Bug",
    "ENHANCEMENT": "Enhancement",
    "DEFECT": "Defect",
    "ISSUE": "Issue",    
    "REFACTOR": "Refactor",
    "RESEARCH": "Research",   
    "TECH_DEBT": "Tech Debt",
    "TEST": "Test",
    "DOC": "Doc",  
}


COMMON_BACKLOG_TYPES = {
    "EPIC": "Epic",
    "USER STORY": "User Story",
    "TASK": "Task",
    "BUG": "Bug",
    "FEATURE": "Feature",
    "ENHANCEMENT": "Enhancement",
    "DEFECT": "Defect",
    "ISSUE": "Issue",
    "REQUIREMENT": "Requirement",
    "CHANGE": "Change",
    "IMPROVEMENT": "Improvement",
    "REFACTOR": "Refactor",
    "RESEARCH": "Research",
    "DESIGN": "Design",
    "ARCHITECTURE": "Architecture",
    "TECH_DEBT": "Tech Debt",
    "TEST": "Test",
    "DOC": "Doc",
    "RELEASE": "Release",
    "DEPLOY": "Deploy",
    "SUPPORT": "Support",
    "TRAINING": "Training",
    "MEETING": "Meeting",
    "WORKSHOP": "Workshop",
    "EVENT": "Event",
    "CONFERENCE": "Conference",
    "SEMINAR": "Seminar",
    "WEBINAR": "Webinar",
    "PRESENTATION": "Presentation",
    "DEMO": "Demo",
    "REVIEW": "Review",
    "RETROSPECTIVE": "Retrospective",
    "PLANNING": "Planning",
    "LEARNING": "Learning",
    "INNOVATION": "Innovation",
    'STRATEGIC THEME': 'Strategic Theme',
    'OBJECTIVE': 'Objective',
    'KEY RESULT': 'Key Result',
    'OKR': 'OKR',
    'KPI': 'KPI',
    'METRIC': 'Metric',
    'GOAL': 'Goal',
    'TARGET': 'Target',
    'INITIATIVE': 'Initiative',
    'PROJECT': 'Project',
    'PROGRAM': 'Program',
    'PORTFOLIO': 'Portfolio',
    'PRODUCT': 'Product',
    'SERVICE': 'Service',
    'APPLICATION': 'Application',
    'PLATFORM': 'Platform',
    'INFRASTRUCTURE': 'Infrastructure',
    'TEAM': 'Team',
    'GROUP': 'Group',
    'DEPARTMENT': 'Department',
    'DIVISION': 'Division',
    'COMPANY': 'Company',
    'ORGANIZATION': 'Organization',
    'COMMUNITY': 'Community',
    'NETWORK': 'Network',
    'MARKET': 'Market',
    'CUSTOMER': 'Customer',
    'USER': 'User',
    'STAKEHOLDER': 'Stakeholder',
    'PARTNER': 'Partner',
    'VENDOR': 'Vendor',
    'RELEASE TRAIN': 'Release Train',
    'VALUE STREAM': 'Value Stream',
    'PRODUCT LINE': 'Product Line',
    'PRODUCT FAMILY': 'Product Family',
    'PRODUCT CATEGORY': 'Product Category',
    'PRODUCT GROUP': 'Product Group',
    'PRODUCT TEAM': 'Product Team',
    'PRODUCT OWNER': 'Product Owner',
    'SCRUM MASTER': 'Scrum Master',
    'TEAM MEMBER': 'Team Member',
    'ADMIN': 'Admin',
    'EDITOR': 'Editor',
    'VIEWER': 'Viewer',
    'MANAGER': 'Manager',
    'CONTRIBUTOR': 'Contributor',
    'DEVELOPER': 'Developer',
    'DESIGNER': 'Designer',
    'UI_UX': 'UI/UX',
    'SYSTEM_ARCHITECT': 'System Architect',
    'ENTERPRISE_ARCHITECT': 'Enterprise Architect',
    'BUSINESS_OWNER': 'Business Owner',
    'PROGRAM_MANAGER': 'Program Manager',
    'PROJECT_MANAGER': 'Project Manager',
    'PORTFOLIO_MANAGER': 'Portfolio Manager',
    'BLOG_ADMIN': 'Blog Admin',
    'COMPONENT': 'Component',
    'MODULE': 'Module',
    'SERVICE': 'Service',
    'FUNCTION': 'Function',
    'CAPABILITY': 'Capability',
    
}

ICON_MAPPING = {
    "EPIC": "fas fa-mountain",
    "STORY": "fas fa-book",
    "TASK": "fas fa-tasks",
    "BUG": "fas fa-bug",
    "FEATURE": "fas fa-star",
    "ENHANCEMENT": "fas fa-wrench",
    "DEFECT": "fas fa-exclamation-triangle",
    "ISSUE": "fas fa-question-circle",
    "REQUIREMENT": "fas fa-list",
    "CHANGE": "fas fa-exchange-alt",
    "IMPROVEMENT": "fas fa-arrow-up",
    "REFACTOR": "fas fa-code",
    "RESEARCH": "fas fa-search",
    "DESIGN": "fas fa-pencil-ruler",
    "ARCHITECTURE": "fas fa-drafting-compass",
    "TECH_DEBT": "fas fa-code-branch",
    "TEST": "fas fa-vial",
    "DOC": "fas fa-file-alt",
    "RELEASE": "fas fa-rocket",
    "DEPLOY": "fas fa-cloud-upload-alt",
    "SUPPORT": "fas fa-life-ring",
    "TRAINING": "fas fa-chalkboard-teacher",
    "MEETING": "fas fa-handshake",
    "WORKSHOP": "fas fa-tools",
    "EVENT": "fas fa-calendar-alt",
    "CONFERENCE": "fas fa-users",
    "SEMINAR": "fas fa-university",
    "WEBINAR": "fas fa-laptop",
    "PRESENTATION": "fas fa-project-diagram",
    "DEMO": "fas fa-play-circle",
    "REVIEW": "fas fa-clipboard-check",
    "RETROSPECTIVE": "fas fa-clock",
    "PLANNING": "fas fa-map",
    "LEARNING": "fas fa-graduation-cap",
    "INNOVATION": "fas fa-lightbulb",
}


COMMON_ROLE_CONFIG = {
    "SCRUM_MASTER": {"name": "Scrum Master", "count": 2},
    "PRODUCT_OWNER": {"name": "Product Owner", "count": 2},
    "TEAM_MEMBER": {"name": "TeamMember", "count": 20},
    "ADMIN": {"name": "Admin", "count": 1},
    "EDITOR": {"name": "Editor", "count": 1},
    "VIEWER": {"name": "Viewer", "count": 2},
    "MANAGER": {"name": "Manager", "count": 2},
    "CONTRIBUTOR": {"name": "Contributor", "count": 2},
    "DEVELOPER": {"name": "Developer", "count": 2},
    "DESIGNER": {"name": "Designer", "count": 2},
    "UI_UX": {"name": "UI/UX", "count": 5},
    "SYSTEM_ARCHITECT": {"name": "System Architect", "count": 5},
    "ENTERPRISE_ARCHITECT": {"name": "Enterprise Architect", "count": 5},
    "BUSINESS_OWNER": {"name": "Business Owner", "count": 5},
    "PROGRAM_MANAGER": {"name": "Program Manager", "count": 5},
    "PROJECT_MANAGER": {"name": "Project Manager", "count": 5},
    "PORTFOLIO_MANAGER": {"name": "Portfolio Manager", "count": 5},
    "BLOG_ADMIN": {"name": "Blog Admin", "count": 5},
    "BLOG_WRITER": {"name": "Blog Writer", "count": 5},
    "BLOG_EDITOR": {"name": "Blog Editor", "count": 5},
    "BLOG_VIEWER": {"name": "Blog Viewer", "count": 5},
    "SITE_ADMIN": {"name": "Site Admin", "count": 1},
    "ORG_ADMIN": {"name": "Org Admin", "count": 1},
    "PROJECT_ADMIN": {"name": "Project Admin", "count": 1},
    "QA": {"name": "QA", "count": 2},
    "ARCHITECT": {"name": "Architect", "count": 2},
    "DEVOPS": {"name": "DevOps", "count": 2},
    "SECURITY": {"name": "Security", "count": 2},
    "BUSINESS_ANALYST": {"name": "Business Analyst", "count": 2},
    "IT_ENGINEER": {"name": "IT Engineer", "count": 2},
    "NETWORK_ENGINEER": {"name": "Network Engineer", "count": 2},
    "TECH_LEAD": {"name": "Tech Lead", "count": 2},
    "TEAM_LEAD": {"name": "Team Lead", "count": 2},
    "PROJECT_LEAD": {"name": "Project Lead", "count": 2},
    "SUPER_USER": {"name": "Super User", "count": 0},
    "NO_ROLE": {"name": "No Role", "count": 0},
}


COMMON_PROJECT_ROLE_CONFIG = {
    "PROJECT_ADMIN": "Admin",
    "PROJECT_EDITOR": "Editor",
    "PROJECT_VIEWER": "Viewer",
    "PROJECT_NOROLE": "No Role",   
}


site_admin_str = COMMON_ROLE_CONFIG['SITE_ADMIN']['name']
org_admin_str = COMMON_ROLE_CONFIG['ORG_ADMIN']['name']
project_admin_str = COMMON_ROLE_CONFIG['PROJECT_ADMIN']['name']

PROJECT_ADMIN_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_ADMIN']
PROJECT_EDITOR_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_EDITOR']
PROJECT_VIEWER_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_VIEWER']
PROJECT_NOROLE_ROLE_STR = COMMON_PROJECT_ROLE_CONFIG['PROJECT_NOROLE']


# PROJECT MEMBER ROLES
PRODUCT_OWNER_STR = COMMON_ROLE_CONFIG['PRODUCT_OWNER']['name']
SCRUM_MASTER_STR = COMMON_ROLE_CONFIG['SCRUM_MASTER']['name']
TEAM_MEMBER_STR = COMMON_ROLE_CONFIG['TEAM_MEMBER']['name']
ARCHITECT_STR = COMMON_ROLE_CONFIG['ARCHITECT']['name']
DEVOPS_STR = COMMON_ROLE_CONFIG['DEVOPS']['name']
SECURITY_STR = COMMON_ROLE_CONFIG['SECURITY']['name']
BUSINESS_ANALYST_STR = COMMON_ROLE_CONFIG['BUSINESS_ANALYST']['name']
QA_STR = COMMON_ROLE_CONFIG['QA']['name']
IT_ENGINEER_STR = COMMON_ROLE_CONFIG['IT_ENGINEER']['name']
NETWORK_ENGINEER_STR = COMMON_ROLE_CONFIG['NETWORK_ENGINEER']['name']
TECH_LEAD_STR = COMMON_ROLE_CONFIG['TECH_LEAD']['name']
TEAM_LEAD_STR = COMMON_ROLE_CONFIG['TEAM_LEAD']['name']
PROJECT_MEMBER_ROLES = [
    PRODUCT_OWNER_STR, SCRUM_MASTER_STR, TEAM_MEMBER_STR, ARCHITECT_STR, DEVOPS_STR, SECURITY_STR, BUSINESS_ANALYST_STR,
    QA_STR, IT_ENGINEER_STR, NETWORK_ENGINEER_STR, TECH_LEAD_STR, TEAM_LEAD_STR
]
################################################################################