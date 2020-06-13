from django.forms import ModelForm, ModelChoiceField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from .models import *

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
            {'name': 'Manage Asset Access Requests', 'url': '/manage_asset_requests'},
            {'name': 'View Asset Acquire Requests', 'url': '/view_asset_acquire_requests'},
            {'name': 'Create New Asset Acquire Requests', 'url': '/create_asset_acquire_request'}
        ],

        'admin': [
            {'name': 'Manage University Assets', 'url': '/manage_university_assets'},
            {'name': 'Add New Software Asset', 'url': '/add_software_asset'},
            {'name': 'Add New Physical Asset', 'url': '/add_physical_asset'},
            {'name': 'Manage Asset Acquire Requests', 'url': '/manage_acquire_requests'},
            {'name': 'Manage Locations', 'url': '/manage_locations'},
            {'name': 'Add New Location', 'url': '/add_location'}
        ]
    }

def get_user_dict(request):
    user = get_user(request)
    user_dict = {
        'username': user.username.upper(),
        'groups': []
    }
    for g in user.groups.all():
        user_dict['groups'].append(g.name.upper())
    return user_dict

def get_inner_asset(id):
    sw = SoftwareAsset.objects.filter(id=id)
    if sw.exists():
        return sw[0]
    ph = PhysicalAsset.objects.filter(id=id)
    if ph.exists():
        return ph[0]
    return False

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
    user_dict = get_user_dict(request)
    actions = []
    for g in user_dict['groups']:
        actions.extend(GROUP_TO_URL[g.lower()])

    return render(request, 'index.html', {'actions': actions, 'user': user_dict})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required
def view_accessed_assets(request):
    user = get_user(request)
    accessed_assets = user.asset_use_set.all()
    return render(request, 'view_accessed_assets.html', {'accessed_assets': accessed_assets})

@login_required
def view_asset(request, id):
    user = get_user(request)
    asset = get_inner_asset(id)
    if not asset:
        return redirect('/view_accessed_assets')

    class SoftwareAssetForm(ModelForm):
        class Meta:
            model = SoftwareAsset
            fields = ('name', 'details', 'contact_person', 'expiry_date', 'vendor', 'version', 'license_key')
    
    class PhysicalAssetForm(ModelForm):
        class Meta:
            model = PhysicalAsset
            fields = ('name', 'details', 'contact_person', 'expiry_date', 'vendor', 'location')

    if isinstance(asset, SoftwareAsset):
        form = SoftwareAssetForm(instance=asset)
    elif isinstance(asset, PhysicalAsset):
        form = PhysicalAssetForm(instance=asset)        

    if asset is not None and user in asset.users.all():
        return render(request, 'view_form.html', {'asset': asset, 'form': form, 'edit': False, 'title': 'View Asset'})

@login_required
def view_asset_access_requests(request):
    user = get_user(request)
    created_requests = AssetAccessRequest.objects.filter(creator=user)
    return render(request, 'view_asset_access_requests.html', {'items': created_requests})

@login_required
def create_asset_access_request(request):
    user = get_user(request)
    class Form(ModelForm):
        class Meta:
            model = AssetAccessRequest
            fields = ('details', 'requested_asset')
    if request.method == 'GET':
        form = Form()      
        return render(request, 'view_form.html', {'form': form, 'edit': True, 'title': 'Create Asset Access Request'})
    
    elif request.method == 'POST':
        details = request.POST['details']
        requested_asset = Asset.objects.get(id=request.POST['requested_asset'])
        creator = user
        request_instance = AssetAccessRequest(details=details, requested_asset=requested_asset, creator=creator)
        request_instance.full_clean()
        request_instance.save()
        return redirect('/view_asset_access_requests')

@login_required
def delete_asset_request(request):
    user = get_user(request)
    try:
        request_id = request.GET["id"]
        asset_request = AssetRequest.objects.filter(id=request_id)
        if asset_request.exists() and asset_request[0].creator == user:
            asset_request.delete()
    except KeyError:
        pass
    return redirect('/')

@login_required
def manage_assets_managed(request):
    user = get_user(request)
    managed_assets = user.asset_manage_set.all()
    return render(request, 'manage_assets_managed.html', {'items': managed_assets, 'delete': False})

@login_required
def edit_asset(request, id):
    user = get_user(request)
    groups = get_user_dict(request)['groups']

    class SoftwareAssetForm(ModelForm):
        class Meta:
            model = SoftwareAsset
            fields = ('name', 'details', 'expiry_date', 'vendor', 'version', 'license_key')
    
    class PhysicalAssetForm(ModelForm):
        class Meta:
            model = PhysicalAsset
            fields = ('name', 'details', 'expiry_date', 'vendor', 'location')

    if request.method == 'GET':
        asset = get_inner_asset(id)
        if not asset:
            return redirect('/manage_assets_managed')
        if isinstance(asset, SoftwareAsset):
            form = SoftwareAssetForm(instance=asset)
        elif isinstance(asset, PhysicalAsset):
            form = PhysicalAssetForm(instance=asset)        

        if asset is not None and ('ADMIN' in groups or user == asset.contact_person):
            return render(request, 'view_form.html', {'asset': asset, 'form': form, 'edit': True, 'title': 'Edit Asset'})

    elif request.method == 'POST':
        asset = get_inner_asset(id)
        asset.name = request.POST['name']
        asset.details = request.POST['details']
        asset.expiry_date = request.POST['expiry_date']
        asset.vendor = request.POST['vendor']
        if isinstance(asset, SoftwareAsset):
            asset.version = request.POST['version']
            asset.license_key = request.POST['license_key']
        else:
            asset.location = Location.objects.get(id=request.POST['location'])
        asset.full_clean()
        asset.save()
        if 'ADMIN' in groups:
            return redirect('/manage_university_assets')
        return redirect('/manage_assets_managed')

@login_required
def manage_asset_requests(request):
    user = get_user(request) 
    asset_requests = []
    for asset in user.asset_manage_set.all():
        asset_requests.extend(asset.assetaccessrequest_set.all())
    return render(request, 'manage_asset_requests.html', {'items': asset_requests})

@login_required
def act_on_request(request, id):
    user = get_user(request)
    asset_request = AssetAccessRequest.objects.get(id=id)
    if asset_request.requested_asset.contact_person == user:
        edit = not (asset_request.approved or asset_request.rejected)
        if request.method == 'POST':
            if edit:
                asset_request.approved = request.POST['action'] == 'approve'
                asset_request.rejected = request.POST['action'] == 'reject'
                asset_request.save()
                if asset_request.approved:
                    requested_asset = asset_request.requested_asset
                    requested_asset.users.add(asset_request.creator)
                    requested_asset.save()
        class Form(ModelForm):
            class Meta:
                model = AssetAccessRequest
                fields = ('creator', 'details', 'requested_asset')
        form = Form(instance=asset_request)
        return render(request, 'act_on_request.html', {'form': form, 'edit': edit, 'title': 'Act on Request'})
    else:
        return redirect('/')

@login_required
def act_on_acquire(request, id):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    asset_request = AssetAcquireRequest.objects.get(id=id)
    edit = not (asset_request.approved or asset_request.rejected)
    if request.method == 'POST':
        if edit:
            asset_request.approved = request.POST['action'] == 'approve'
            asset_request.rejected = request.POST['action'] == 'reject'
            asset_request.save()
            return redirect('/manage_acquire_requests')
    class Form(ModelForm):
        class Meta:
            model = AssetAcquireRequest
            fields = ('creator', 'details', 'requested_asset_detail')
    form = Form(instance=asset_request)
    return render(request, 'act_on_request.html', {'form': form, 'edit': edit, 'title': 'Act on Acquire Request'})

@login_required
def view_asset_acquire_requests(request):
    user = get_user(request)
    created_requests = AssetAcquireRequest.objects.filter(creator=user)
    return render(request, 'view_asset_acquire_requests.html', {'items': created_requests})

@login_required
def create_asset_acquire_request(request):
    user = get_user(request)
    class Form(ModelForm):
        class Meta:
            model = AssetAcquireRequest
            fields = ('details', 'requested_asset_detail')
    if request.method == 'GET':
        form = Form()      
        return render(request, 'view_form.html', {'form': form, 'edit': True, 'title': 'Create Asset Acquire Request'})
    
    elif request.method == 'POST':
        details = request.POST['details']
        requested_asset_detail = request.POST['requested_asset_detail']
        creator = user
        request_instance = AssetAcquireRequest(details=details, requested_asset_detail=requested_asset_detail, creator=creator)
        request_instance.full_clean()
        request_instance.save()
        return redirect('/view_asset_acquire_requests')

@login_required
def manage_university_assets(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    assets = Asset.objects.all()
    return render(request, 'manage_assets_managed.html', {'items': assets, 'delete': True})

@login_required
def add_software_asset(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    
    class SoftwareAssetForm(ModelForm):
        class Meta:
            model = SoftwareAsset
            exclude = ('id', 'users')

    if request.method == 'GET':
        form = SoftwareAssetForm()       
        return render(request, 'view_form.html', {'form': form, 'edit': True, 'title': 'Add Software Asset'})

    elif request.method == 'POST':
        asset = SoftwareAsset()
        asset.name = request.POST['name']
        asset.details = request.POST['details']
        asset.expiry_date = request.POST['expiry_date']
        asset.vendor = request.POST['vendor']
        asset.version = request.POST['version']
        asset.license_key = request.POST['license_key']
        asset.conact_person = User.objects.get(id=request.POST['contact_person'])
        asset.full_clean()
        asset.save()
        return redirect('/manage_university_assets')

@login_required
def add_physical_asset(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')

    class PhysicalAssetForm(ModelForm):
        class Meta:
            model = PhysicalAsset
            exclude = ('id', 'users')

    if request.method == 'GET':
        form = PhysicalAssetForm()       
        return render(request, 'view_form.html', {'form': form, 'edit': True, 'title': 'Add Physical Asset'})

    elif request.method == 'POST':
        asset = PhysicalAsset()
        asset.name = request.POST['name']
        asset.details = request.POST['details']
        asset.expiry_date = request.POST['expiry_date']
        asset.vendor = request.POST['vendor']
        asset.location = Location.objects.get(id=request.POST['location'])
        asset.conact_person = User.objects.get(id=request.POST['contact_person'])
        asset.full_clean()
        asset.save()
        return redirect('/manage_university_assets')

@login_required
def manage_acquire_requests(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    asset_requests = AssetAcquireRequest.objects.all()
    return render(request, 'manage_acquire_requests.html', {'items': asset_requests})

@login_required
def manage_locations(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    locations = Location.objects.all()
    return render(request, 'manage_locations.html', {'items': locations, 'delete': True})

@login_required
def delete_location(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')
    try:
        location_id = request.GET["id"]
        location = Location.objects.filter(id=location_id)
        if location.exists():
            location.delete()
    except KeyError:
        pass
    return redirect('/')

@login_required
def add_location(request):
    groups = get_user_dict(request)['groups']
    if 'ADMIN' not in groups:
        return redirect('/')

    class Form(ModelForm):
        class Meta:
            model = Location
            exclude = ('id',)

    if request.method == 'GET':
        form = Form()       
        return render(request, 'view_form.html', {'form': form, 'edit': True, 'title': 'Add Location'})

    elif request.method == 'POST':
        location = Location()
        location.manager = User.objects.get(id=request.POST['manager'])
        location.room_number = request.POST['room_number']
        location.full_clean()
        location.save()
        return redirect('/manage_locations')
