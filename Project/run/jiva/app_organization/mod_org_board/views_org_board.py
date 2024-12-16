
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_board.models_org_board import *
from app_organization.mod_org_board.forms_org_board import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog_super_type.models_backlog_super_type import *
from app_organization.mod_backlog_type.models_backlog_type import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_boards'
module_path = f'mod_org_board'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_org_boards(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OrgBoard.objects.filter(active=False, deleted=False,
                                org_id=org_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
             
        if 'selected_item' in request.POST:  # Correct the typo here
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  # Ensure item_id is converted to int if necessary
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_boards', org_id=org_id)
            return redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_boards',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_org_boards.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_boards(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=False, deleted=False, org_id=org_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_boards', org_id=org_id)
                redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_boards',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_boards.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_board(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgBoardForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Board',
    }
    template_file = f"{app_name}/{module_path}/create_org_board.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgBoardForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Board',
    }
    template_file = f"{app_name}/{module_path}/edit_org_board.html"
    return render(request, template_file, context)



@login_required
def delete_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Board',
    }
    template_file = f"{app_name}/{module_path}/delete_org_board.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Board',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_board.html"
    return render(request, template_file, context)


@login_required
def restore_org_board(request,  org_id, org_board_id):
    user = request.user
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_boards', org_id=org_id)
   


@login_required
def view_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Board',
    }
    template_file = f"{app_name}/{module_path}/view_org_board.html"
    return render(request, template_file, context)


# @login_required
# def view_project_board(request, project_id):
#     user = request.user
#     project = Project.objects.get(id=project_id, active=True)
#     org_id = project.org.id
#     organization = project.org
    
#     # Backlog collections
#     flat_backlog_root = Backlog.objects.filter(pro=project, name=FLAT_BACKLOG_ROOT_NAME).first()
#     flat_backlog_collection_type = BacklogType.objects.filter(name='Collection').first() 
#     backlog_collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root, active=True)
#     # send the backlog details of the project
#     backlog_types = BacklogType.objects.filter(
#         active=True, 
#         name__in=FLAT_BACKLOG_TYPES.values(), 
#     ).select_related('type')
#     filters = {}
    
#     backlog_items = Backlog.objects.filter(
#             pro_id=project.id,
#             type__in=backlog_types, 
#             **filters,
#             active=True
#         ).order_by('position', '-created_at')
    
    
#     # Check the project default board
#     DEFAULT_BOARD_NAME = 'Default Board'
#     project_board = ProjectBoard.objects.filter(project=project, active=True, name=DEFAULT_BOARD_NAME).first()
#     if not project_board:
#         project_board = ProjectBoard()
#         project_board.name = DEFAULT_BOARD_NAME
#         project_board.project = project
#         project_board.author = user
#         project_board.save()
    
#     DEFAULT_BOARD_COLUMNS = ['Backlog', 'ToDo', 'In Progress', 'Blocked', 'Done']
#     # Column is internally called as state
#     for column_name in DEFAULT_BOARD_COLUMNS:
#         column = ProjectBoardState.objects.filter(board=project_board, name=column_name).first()
#         if not column:
#             column = ProjectBoardState()
#             column.name = column_name
#             column.board = project_board
#             column.author = user
#             column.save()
    
#     project_board_states = ProjectBoardState.objects.filter(board=project_board, active=True)
    
#     # Categorize backlog items by their current state
#     state_items = {state.name: [] for state in project_board_states}
#     for item in backlog_items:
#         if item.state and item.state.name in state_items:
#             state_items[item.state.name].append(item)

#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'project_board',
#         'organization': organization,
#         'org_id': org_id,
#         'project': project,
#         'pro_id': project.id,
#         'org': organization,
#         'backlog_items': state_items.get('Backlog', []),
#         'todo_items': state_items.get('ToDo', []),
#         'in_progress_items': state_items.get('In Progress', []),
#         'blocked_items': state_items.get('Blocked', []),
#         'done_items': state_items.get('Done', []),
#         'backlog_collections': backlog_collections,
#         'project_board': project_board,
#         'project_board_states': project_board_states,
        
#         'module_path': module_path,        
#         'page_title': f'Project Board: '+project.name,
#     }
#     template_file = f"{app_name}/{module_path}/project/view_project_board.html"
#     return render(request, template_file, context)


@login_required
def view_project_board(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog collections
    flat_backlog_root = Backlog.objects.filter(pro=project, name=FLAT_BACKLOG_ROOT_NAME).first()
    flat_backlog_collection_type = BacklogType.objects.filter(name='Collection').first() 
    backlog_collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root, active=True)
    # send the backlog details of the project
    backlog_types = BacklogType.objects.filter(
        active=True, 
        name__in=FLAT_BACKLOG_TYPES.values(), 
    ).select_related('type')
    filters = {}
    # Get or create the default project board
    DEFAULT_BOARD_NAME = 'Default Board'
    project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )

    # Ensure the default columns exist
    DEFAULT_BOARD_COLUMNS = ['Backlog', 'ToDo', 'In Progress', 'Blocked', 'Done']
    backlog_state = None  # To store the "Backlog" state reference
    for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
        state, _ = ProjectBoardState.objects.get_or_create(
            board=project_board,
            name=column_name,
            defaults={'author': user, 'wip_limit': 0}
        )
        if column_name == 'Backlog':
            backlog_state = state


    # Fetch unlinked backlog items
    project_backlog_items = Backlog.objects.filter(
        pro_id=project.id,
        type__in=backlog_types, 
        **filters,
        active=True
    ).exclude(
        id__in=ProjectBoardCard.objects.filter(board=project_board).values_list('backlog_id', flat=True)
    ).order_by('position', '-created_at')
    project_board_states = ProjectBoardState.objects.filter(board=project_board)
    # Link unlinked backlog items to the Backlog state
    if backlog_state:
        for backlog_item in project_backlog_items:
            print(f">>> === Adding backlog_item: {backlog_item} to Backlog state === <<<")
            ProjectBoardCard.objects.create(
                backlog=backlog_item,
                board=project_board,
                state=backlog_state,
            )

    
    
    # Fetch the project backlog items state
    state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
    print(f">>> === Board States: {state_items} === <<<")
    # Get the card / backlog item from the ProjectBoardStateTransition
    for state in project_board_states:
        state_items[state.name] = ProjectBoardCard.objects.filter(board=project_board, state=state)
    
    print(f">>> === state_items: {state_items} === <<<")
    print(f">>> === Backlog: { state_items.get('Backlog', [])} === <<<")
    print(f">>> === Todo: { state_items.get('ToDo', [])} === <<<")
    print(f">>> === InProgress: { state_items.get('In Progress', [])} === <<<")
    print(f">>> === Blocked: { state_items.get('Blocked', [])} === <<<")
    print(f">>> === Done: { state_items.get('Done', [])} === <<<")
    
    # # Get the current card state from the transition model
    # for state in project_board_states:
    #     transitions = ProjectBoardStateTransition.objects.filter(card__board=project_board, to_state=state)
    #     state_items[state.name] = [transition.card for transition in transitions]

    
    test_backlog = state_items.get('Backlog', [])
    print(f">>> === test_backlog: {test_backlog} === <<<")

    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': project_board,
        'project_board_states': project_board_states,
        'backlog_items': state_items.get('Backlog', []),
        'todo_items': state_items.get('ToDo', []),
        'in_progress_items': state_items.get('In Progress', []),
        'blocked_items': state_items.get('Blocked', []),
        'done_items': state_items.get('Done', []),
        'page_title': f'Project Board: {project.name}',
    }

    template_file = f"{app_name}/{module_path}/project/view_project_board.html"
    return render(request, template_file, context)

@login_required
def ajax_update_project_board_card_state(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            from_state_id = data.get('from_state_id')
            to_state_id = data.get('to_state_id')

            if not (card_id and from_state_id and to_state_id):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Fetch the card and states
            card = ProjectBoardCard.objects.get(id=card_id)
            from_state = ProjectBoardState.objects.get(id=from_state_id)
            to_state = ProjectBoardState.objects.get(id=to_state_id)

            # Validate that the card belongs to the current state
            if card.state != from_state:
                return JsonResponse({"error": "Card state mismatch"}, status=400)

            # Update the card's state
            card.state = to_state
            card.save()

            # Log the transition
            created_st_entry = ProjectBoardStateTransition.objects.create(
                card=card.backlog,
                from_state=from_state,
                to_state=to_state,
                transition_time=now(),

            )
            
            st_count = ProjectBoardStateTransition.objects.all().count()
            print(f">>> === st_count: {st_count}: {created_st_entry} === <<<")

            return JsonResponse({
                "message": "Card state updated successfully",
                "card_id": card.id,
                "from_state": from_state.name,
                "to_state": to_state.name,
            })

        except ProjectBoardCard.DoesNotExist:
            return JsonResponse({"error": "Card does not exist"}, status=404)
        except ProjectBoardState.DoesNotExist:
            return JsonResponse({"error": "State does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

# # Update
# @login_required
# def ajax_update_project_board_card_state(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             card_id = data.get('card_id')
#             from_state_id = data.get('from_state_id')
#             to_state_id = data.get('to_state_id')

#             print(f">>> === data: {data} === <<<")  # Debugging the input data

#             if not (card_id and from_state_id and to_state_id):
#                 return JsonResponse({"error": "Missing required fields"}, status=400)

#             # Fetch the states
#             from_state = ProjectBoardState.objects.get(id=from_state_id)
#             to_state = ProjectBoardState.objects.get(id=to_state_id)

#             # Create the transition
#             transition = ProjectBoardStateTransition.objects.create(
#                 card=from_state,
#                 from_state=from_state,
#                 to_state=to_state,
#                 transition_time=now()
#             )

#             # Update the card's state (assuming `state` field is on the card)
#             from_state.save()
#             to_state.save()

#             return JsonResponse({
#                 "message": "Card state updated successfully",
#                 "transition_id": transition.id,
#                 "from_state": from_state.name if from_state.name else str(from_state.id),
#                 "to_state": to_state.name if to_state.name else str(to_state.id),
#                 "transition_time": transition.transition_time
#             })
#         except ProjectBoardState.DoesNotExist:
#             return JsonResponse({"error": "State does not exist"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)