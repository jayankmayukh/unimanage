from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user

GROUP_TO_URL = {
        'student': [
            {'name': 'View Accessed Assets', 'url': '/view_accessed_assets'},
            {'name': 'View Asset Access Requests', 'url': '/view_asset_access_requests'},
            {'name': 'Create New Asset Access Requests', 'url': '/create_asset_access_request'}
        ],

        'professor': [
            {'name': 'View Accessed Assets', 'url': '/view_accessed_assets'},
            {'name': 'View Asset Access Requests', 'url': '/view_asset_access_requests'},
            {'name': 'Create New Asset Access Requests', 'url': '/create_asset_access_request'},
            {'name': 'Manage Assets Managed By Me', 'url': '/manage_assets_managed'},
            {'name': 'Manage Asset Access Requests', 'url': '/mange_asset_requests'},
            {'name': 'View Locations Manged By Me', 'url': '/view_locations_manged'},
            {'name': 'View Asset Acquire Requests', 'url': '/view_asset_acquire_requests'},
            {'name': 'Create New Asset Acquire Requests', 'url': '/create_asset_acquire_request'}
        ],

        'admin': [
            {'name': 'Manage University Assets', 'url': '/manage_university_assets'},
            {'name': 'Add New Asset', 'url': '/add_new_asset'},
            {'name': 'Manage Asset Acquire Requests', 'url': '/manage_asset_acquire_requests'},
            {'name': 'Manage Locations', 'url': '/manage_locations'},
            {'name': 'Add New Location', 'url': '/add_new_location'}
        ]
    }

def login_view(request):
    if get_user(request).is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'failed_attempt': True})
    else:
        return render(request, 'login.html', {'failed_attempt': False})

@login_required
def index(request):
    user = get_user(request)        
    user_dict = {
        'username': user.username.upper(),
        'groups': []
    }
    actions = []
    for g in user.groups.all():
        user_dict['groups'].append(g.name.upper())
        actions.extend(GROUP_TO_URL[g.name])

    return render(request, 'index.html', {'actions': actions, 'user': user_dict})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')