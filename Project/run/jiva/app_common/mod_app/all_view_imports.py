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