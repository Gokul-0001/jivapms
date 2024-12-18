from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_collection.models_collection import *

from app_organization.mod_step.models_step import *
from app_jivapms.mod_app.all_view_imports import *

from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'

@login_required
def view_project_tree_backlog(request, pro_id):
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=pro_id)
    
    # IMPORTANT items
    # 1. Backlog Super Type
    # 2. Backlog Type
    # 3. Backlog
     
    # 1. Backlog Super Type
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_super_type, created = BacklogSuperType.objects.get_or_create(pro=project, name=pbst_name)
    logger.debug(f">>> === BACKLOG SUPER TYPE: {project_backlog_super_type} {project_backlog_super_type.id} === <<<")
    
    # 2. Backlog Type
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    logger.debug(f">>> === BACKLOG TYPE: {project_backlog_type} {project_backlog_type.id} === <<<")
    
    # 2.1 Create the Backlog Type from the Config as a Schema
    # 2.1.1 Get the Config
    config = PROJECT_WBS_TREE_CONFIG
    
    # 2.1.2 Create the Backlog Type from the Config as a Schema
    created_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    
    # 2.1.3 Get the Backlog Types
    # Display the structure of the created node
    tree_structure = list_tree_structure(created_node)

    # Optional: Log or return the structure for further use
    logger.info("\n".join(tree_structure))
        
    # vars
    backlog_deleted = False
    backlog_deleted_count = 0
    backlog_items = []
    backlog_types = []
    backlog_items_count = 0
    
    
    # get backlog types
    
    
    # get backlog items
    backlog_items = Backlog.objects.filter(pro=project).order_by('position', '-created_at')

    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'view_project_tree_backlog',
        'user': user,
        'member': member,
        'pro': project,
        'project': project,
        'pro_id': pro_id,
        'org': project.org,
        'org_id': project.org_id,
        
        'backlog_deleted': backlog_deleted,
        'backlog_deleted_count': backlog_deleted_count,
        'backlog_items': backlog_items,
        'backlog_types': backlog_types,
        'backlog_items_count': backlog_items_count,
        
        'page_title': f'View Project Tree Backlog',
        "STATUS_CHOICES": STATUS_CHOICES,
        "SIZE_CHOICES": SIZE_CHOICES,
        "FLAT_BACKLOG_NAME_ICONS": FLAT_BACKLOG_NAME_ICONS,
        'COMMON_BACKLOG_TYPES': COMMON_BACKLOG_TYPES,
        'ICON_MAPPING': ICON_MAPPING,
    }       
    template_file = f"{app_name}/{module_path}/view_project_tree_backlog.html"
    return render(request, template_file, context)

def list_tree_structure(node, level=0):
    """
    Recursively lists the tree structure starting from the given node.
    
    Args:
        node (Model): The root node from which to start listing.
        level (int): The current depth level (used for indentation).

    Returns:
        list: A nested representation of the tree structure.
    """
    tree_structure = []
    indent = " " * (level * 4)  # Indentation for display
    tree_structure.append(f"{indent}- {node.name} (ID: {node.id})")
    
    # Recursively list child nodes
    for child in node.get_active_children():
        tree_structure.extend(list_tree_structure(child, level=level + 1))
    
    return tree_structure


def create_or_update_tree_from_config(config, model_name, parent=None, project=None):
    """
    Creates or updates tree nodes in the database based on a configuration dictionary.

    Args:
        config (dict): The tree structure as a dictionary.
        model_name (str): The name of the model, including the app name (e.g., "myapp.BacklogSuperType").
        parent (Model): The parent node (None for the root).
        project (Model): The project this tree belongs to.

    Returns:
        Model: The root node or updated tree node.
    """
    from django.apps import apps

    # Resolve the model from the model_name string
    model = apps.get_model(model_name)

    # Find or create the current node
    node, created = model.objects.get_or_create(
        pro=project,
        name=config["name"],
        parent=parent,
        defaults={"name": config["name"]}  # Add any default values for fields here
    )

    if created:
        logger.debug(f"Created new node: {node.name}")
    else:
        logger.debug(f"Node already exists: {node.name}")

    # Compare and update children
    existing_children = list(node.get_active_children())
    config_children = config.get("children", [])

    # Match existing children to configuration
    matched_children = set()
    for child_config in config_children:
        # Check for a matching child
        matching_child = next(
            (child for child in existing_children if child.name == child_config["name"]),
            None
        )
        if matching_child:
            # Recursively update the child
            create_or_update_tree_from_config(
                child_config, model_name, parent=node, project=project
            )
            matched_children.add(matching_child)
        else:
            # Create a new child node
            create_or_update_tree_from_config(
                child_config, model_name, parent=node, project=project
            )

    # Remove unmatched existing children
    unmatched_children = [child for child in existing_children if child not in matched_children]
    for unmatched_child in unmatched_children:
        logger.warning(f"Unmatched child node found in DB: {unmatched_child.name}. Consider deleting.")

    return node


def create_tree_from_config(config, model_name, parent=None, project=None):
    """
    Recursively creates tree nodes in the database from a configuration dictionary.

    Args:
        config (dict): The tree structure as a dictionary.
        model_name (str): The name of the model, including the app name (e.g., "myapp.BacklogSuperType").
        parent (Model): The parent node (None for the root).
        project (Model): The project this tree belongs to.

    Returns:
        Model: The created node.
    """
    # Resolve the model from the model_name string
    model = apps.get_model(model_name)
    
    # Create the current node
    node = model.objects.create(
        pro=project,
        name=config["name"],
        parent=parent  # Assuming the model has a `parent` field for hierarchical relations
    )
    
    # Recursively create child nodes if present
    children = config.get("children", [])
    for child_config in children:
        create_tree_from_config(child_config, model_name=model_name, parent=node, project=project)
    
    return node



def generate_jstree_data(node):
    """
    Recursively generate jsTree-compatible data from the BacklogType tree.

    Args:
        node (BacklogType): The root node to start from.

    Returns:
        dict: jsTree-compatible JSON representation of the tree.
    """
    # Base node format for jsTree
    jstree_node = {
        "id": node.id,         # Unique identifier for the node
        "text": node.name,     # Display name of the node
        "children": [],        # List to hold child nodes
        "type": node.parent.name if node.parent else "root"  # Node type
    }

    # Recursively add child nodes
    for child in node.get_active_children():  # Use 'Project' as the related_name
        jstree_node["children"].append(generate_jstree_data(child))

    return jstree_node
