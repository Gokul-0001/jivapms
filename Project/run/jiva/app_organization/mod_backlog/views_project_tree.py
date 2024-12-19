from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_collection.models_collection import *

from app_organization.mod_step.models_step import *
from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *

from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'



# Sequence the backlog items for addition at top
def seq_add_to_top(ajax_data):
    seq = 2
    new_data = ajax_data.replace("[",'')
    new_data = new_data.replace("]",'')
    sorted_list = new_data.split(",")
    for item in sorted_list:
        str = item.replace('"','')
        position = str.split('_')
        Backlog.objects.filter(pk=position[0]).update(position=seq)
        logger.debug(f">>> === SEQ ADD TO TOP: {position[0]} with {seq} === <<<")
        seq += 1

@login_required
def view_project_tree_backlog(request, pro_id):
        
    # vars
    backlog_deleted = False
    backlog_deleted_count = 0
    backlog_items = []
    backlog_types = []
    backlog_items_count = 0
    
    
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
    
    # 2.1.4 Get the Backlog Types as a ref dictionary {name: id}   
    bt_tree_name_and_id = get_tree_name_id(created_node)
    logger.debug(f"Backlog Type Tree Name ID: {bt_tree_name_and_id}")
    
    # 2.2 Get the Epic level id and its children
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id, active=True)
    epic_type_parent = epic_type_node.parent
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    logger.debug(f">>> === EPIC TYPE: {epic_type_node} {epic_type_id} {backlog_types} === <<<")
    
    
    # 3. Backlog
    # 3.1 Create the Backlog Project Tree Root Node
    pb_name = f"{project.id}_PROJECT_TREE"
    project_backlog, created = Backlog.objects.get_or_create(pro=project, name=pb_name, type=project_backlog_type)
    logger.debug(f">>> === BACKLOG: {project_backlog} {project_backlog.id} === <<<")
    
    # 3.2 Test creation
    # create a backlog item, here you can create a backlog item with the type you want and Project Parent as root node
    # later we can move that to the desired location
    # backlog_item_name = "Test Epic - CHECK"
    # backlog_item_type_id = bt_tree_name_id.get("Epic")
    # created_bi = Backlog.objects.create(pro=project, name=backlog_item_name, parent=project_backlog, type_id=backlog_item_type_id)
    # logger.debug(f">>> === BACKLOG ITEM: {created_bi} {created_bi.id} {created_bi.type}=== <<<")
    # list_created = Backlog.objects.filter(pro=project, parent=project_backlog, type_id=backlog_item_type_id)
    # logger.debug(f">>> === BACKLOG ITEM: {created_bi} {created_bi.id} === <<<")
    # logger.debug(f">>> === BACKLOG ITEM LIST: {list_created} === <<<")
    
    # 3.3 Get the Backlog Items
    
    strategic_theme_id = bt_tree_name_and_id.get("Strategic Theme")
    initiative_id = bt_tree_name_and_id.get("Initiative")
    exclude_types = [strategic_theme_id, initiative_id]
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id, feature_type_id, component_type_id, capability_type_id]
    #backlog_epic_items = Backlog.objects.filter(pro=project, parent=project_backlog).exclude(type__in=exclude_types)
    backlog_epic_items = Backlog.objects.filter(pro=project, type__in=include_types, active=True)
    #backlog_epic_items = Backlog.objects.filter(pro=project, parent=project_backlog)
    backlog_epic_items_count = backlog_epic_items.count()
    logger.debug(f">>> === BACKLOG ITEMS: {backlog_epic_items_count} {backlog_epic_items} === <<<")


    # 3.4 Get the epics of this backlog
    epics_in_backlog = Backlog.objects.filter(pro=project, type=epic_type_id, active=True)
    #epics_in_backlog = {epic.id: epic for epic in backlog_epic_items if epic.type.id == epic_type_id}
    logger.debug(f">>> === EPICS IN THIS BACKLOG: {epics_in_backlog} === <<<")
    
    backlog_summary = request.POST.get('backlog_summary')
    add_action = request.POST.get('add_action')
    action = request.POST.get('read_action', '').strip().lower()
    collection_id = request.POST.get("collection_id")
    selected_items = request.POST.get("selected_items", "").split(",")
    type_of_bi = request.POST.get("type")
    ajax_data = request.POST.get("seq_list_data")
    logger.debug(f">>> === AJAX DATA: {ajax_data} === <<<")
    display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=include_types)
    logger.debug(f">>> === DISPLAY DATA : {display_backlog_items} === <<<")
    test_display = None
    
    if action == 'assign':
        logger.debug(f">>> === Assigning Items: {selected_items} to Collection: {collection_id} === <<<")
        for each_item in selected_items:
            backlog_item = Backlog.objects.get(id=each_item)
            if collection_id == 'Others':
                backlog_item.parent = project_backlog
            elif collection_id == "deleted":
                backlog_item.active = False
            else:
                backlog_item.parent = Backlog.objects.get(id=collection_id)
            backlog_item.save() 
      
        logger.debug(f">>> === Items {selected_items} assigned to collection {collection_id} successfully! === <<<")
        return redirect("view_project_tree_backlog", pro_id=pro_id)
       
    elif action == "unassign":
        logger.debug(f">>> === UnAssigning Items: {selected_items} from Collection: {collection_id} === <<<")
        for each_item in selected_items:
            backlog_item = Backlog.objects.get(id=each_item)
            backlog_item.parent = project_backlog
            if collection_id == "deleted":
                backlog_item.active = True
            backlog_item.save()
        #display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=include_types)
        logger.debug(f">>> === Items {selected_items} unassigned from collection {collection_id} successfully! === <<<")
        
        return redirect("view_project_tree_backlog", pro_id=pro_id)
    else:        
        logger.debug(f">>> === Invalid action: {action} === <<<")
            
    
    
    if add_action == 'add':
        logger.debug(f">>> === ADD ACTION: {add_action} === <<<")
        if 'add_to_top' in request.POST:
            logger.debug(f">>> === ADD TO TOP:  === <<<")
            
            # Create the new backlog item with a temporary position
            create_backlog_item = Backlog.objects.create(
                pro=project,
                name=backlog_summary,
                parent=project_backlog,
                position=0,  # Temporary; will be updated
                created_by=user,
                type_id=type_of_bi
            )
            
            # Update positions of existing items
            Backlog.objects.filter(pro=project, parent=project_backlog, active=True).exclude(id=create_backlog_item.id).update(
                position=models.F('position') + 1
            )

            # Set the new item's position to 1
            create_backlog_item.position = 1
            create_backlog_item.save()

            # Regenerate display_backlog_items
            backlog_epic_items = Backlog.objects.filter(pro=project, active=True, type__in=include_types)
            seq_add_to_top(ajax_data)
            logger.debug(f">>> === ADD TO TOP: {create_backlog_item} {create_backlog_item.id} === <<<")

            
        if 'add_to_bottom' in request.POST:
            logger.debug(f">>> === ADD TO BOTTOM:  === <<<")

            # Find the current maximum position in the existing items
            max_position = Backlog.objects.filter(pro=project, parent=project_backlog, active=True).aggregate(
                max_position=models.Max('position')
            )['max_position'] or 0  # Default to 0 if no items exist

            # Create the new backlog item with the next available position
            create_backlog_item = Backlog.objects.create(
                pro=project,
                name=backlog_summary,
                parent=project_backlog,
                position=max_position + 1,  # Next position
                created_by=user,
                type_id=type_of_bi
            )

            # Regenerate display_backlog_items
            logger.debug(f">>> === ADD TO BOTTOM: {create_backlog_item} {create_backlog_item.id} === <<<")
            return redirect("view_project_tree_backlog", pro_id=pro_id)


    
    # test
    logger.debug(f">>> === EPICS IN THIS BACKLOG: {epics_in_backlog} === <<<")
    
    
    backlog_items_count = len(display_backlog_items)
    logger.debug(f">>> === BACKLOG ITEMS COUNT: {display_backlog_items} === <<<")
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
        
        'backlog_epic_items': backlog_epic_items,
        
        'backlog_deleted': backlog_deleted,
        'backlog_deleted_count': backlog_deleted_count,
        'backlog_items': backlog_items,
        'backlog_types': backlog_types,
        'backlog_items_count': backlog_items_count,
        'backlog_types_count': backlog_types_count,
        'display_backlog_items': display_backlog_items,
        
        'epics_in_backlog': epics_in_backlog,
        'epic_type_parent': epic_type_parent,

        
        'project_backlog_super_type_url': f"/org/backlog_super_type/list_backlog_super_types/{pro_id}/",
        'project_backlog_type_url': f"/org/backlog_type/list_backlog_types/{pro_id}/{project_backlog_type.id}/",
        'project_backlog_url': f"/org/backlog/list_backlogs/{pro_id}/{project_backlog.id}/",
        
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


def get_tree_name_id(node, level=0):
    """
    Recursively lists the tree structure starting from the given node.
    
    Args:
        node (Model): The root node from which to start listing.
        level (int): The current depth level (used for indentation).

    Returns:
        list: A nested representation of the tree structure.
    """
    tree_structure = {}
    node_details = {node.name: node.id}
    tree_structure.update(node_details)
    
    # Recursively list child nodes
    for child in node.get_active_children():
        tree_structure.update(get_tree_name_id(child, level=level + 1))
    
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


# create an ajax function to edit, move, delete, add backlog item
