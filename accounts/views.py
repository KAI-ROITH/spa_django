# accounts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import RetailAsset, ITAsset, Outlet, Service, NetworkAsset
from .forms import RetailAssetForm, ITAssetForm, ServiceForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import json


# ============================================
# Authentication Views
# ============================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validate that both fields are provided
        if not username or not password:
            return render(request, 'accounts/login.html', {
                'error': 'Please provide both username and password.'
            })
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password. Please try again.'
            })
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validate inputs
        if not username or not password:
            return render(request, 'accounts/register.html', {
                'error': 'Please provide both username and password.'
            })
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists. Please choose another.'
            })
        
        # Create new user
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    
    return render(request, 'accounts/register.html')


# ============================================
# Dashboard View
# ============================================

@login_required
def dashboard(request):
    retail_count = RetailAsset.objects.count()
    it_count = ITAsset.objects.count()
    network_count = NetworkAsset.objects.count()
    total = retail_count + it_count + network_count
    labels = ['Retail', 'IT', 'Network']
    data = [retail_count, it_count, network_count]
    return render(request, 'accounts/dashboard.html', {
        'stats': {
            'total_assets': total,
            'retail_assets': retail_count,
            'it_assets': it_count,
            'network_assets': network_count,
        },
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })


# ============================================
# Asset ID Generation API Views
# ============================================

@login_required
def get_next_retail_asset_id(request):
    """API endpoint to get the next available Retail asset ID"""
    item_name = request.GET.get('item', '')
    if item_name:
        next_id = RetailAsset.generate_asset_id(item_name)
        return JsonResponse({'asset_id': next_id})
    return JsonResponse({'error': 'Item name required'}, status=400)


@login_required
def get_next_it_asset_id(request):
    """API endpoint to get the next available IT asset ID"""
    asset_type = request.GET.get('asset_type', '')
    if asset_type:
        next_id = ITAsset.generate_asset_id(asset_type)
        return JsonResponse({'asset_id': next_id})
    return JsonResponse({'error': 'Asset type required'}, status=400)


# ============================================
# Retail Assets Views
# ============================================

@login_required
def retail_assets(request):
    assets = RetailAsset.objects.all().select_related('outlet')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    outlet_filter = request.GET.get('outlet', '')
    status_filter = request.GET.get('status', '')
    brand_filter = request.GET.get('brand', '')
    
    # Apply filters
    if search_query:
        assets = assets.filter(
            Q(item__icontains=search_query) |
            Q(sn__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(asset_id__icontains=search_query)
        )
    
    if outlet_filter:
        assets = assets.filter(outlet_id=outlet_filter)
    
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    if brand_filter:
        assets = assets.filter(brand__icontains=brand_filter)
    
    assets = assets.order_by('-date_purchase')
    
    # Get filter options
    outlets = Outlet.objects.all()
    statuses = RetailAsset.STATUS_CHOICES
    brands = RetailAsset.objects.values_list('brand', flat=True).distinct()
    
    return render(request, 'accounts/retail_assets.html', {
        'assets': assets,
        'outlets': outlets,
        'statuses': statuses,
        'brands': brands,
        'search_query': search_query,
        'selected_outlet': outlet_filter,
        'selected_status': status_filter,
        'selected_brand': brand_filter,
    })


@login_required
def retail_asset_detail(request, id):
    asset = get_object_or_404(RetailAsset, id=id)
    services = Service.objects.filter(asset=asset).order_by('-service_date')
    return render(request, 'accounts/retail_asset_detail.html', {
        'asset': asset,
        'services': services
    })


@login_required
def add_retail_asset(request):
    if request.method == 'POST':
        form = RetailAssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            
            # If asset_id is empty, generate it
            if not asset.asset_id:
                asset.asset_id = RetailAsset.generate_asset_id(asset.item)
            
            # Handle user field
            asset.user = request.POST.get('user', '')
            
            asset.status = 'Active' if form.cleaned_data.get('active') else (asset.status or 'Draft')
            asset.save()
            return redirect('retail_assets')
    else:
        form = RetailAssetForm()
    return render(request, 'accounts/add_retail_asset.html', {'form': form})


@login_required
def edit_retail_asset(request, pk):
    """Edit an existing Retail asset"""
    asset = get_object_or_404(RetailAsset, pk=pk)
    outlets = Outlet.objects.all()
    
    if request.method == 'POST':
        try:
            # Get the outlet
            outlet_id = request.POST.get('outlet')
            outlet = get_object_or_404(Outlet, pk=outlet_id) if outlet_id else None
            
            # Update asset fields
            asset.asset_id = request.POST.get('asset_id', asset.asset_id)
            asset.item = request.POST.get('item', '')
            asset.brand = request.POST.get('brand', '')
            asset.model = request.POST.get('model', '')
            asset.sn = request.POST.get('sn', '')
            asset.power_input = request.POST.get('power_input', '')
            asset.user = request.POST.get('user', '')
            asset.allocation = request.POST.get('allocation', '')  # ← ADDED THIS LINE
            asset.outlet = outlet
            asset.status = request.POST.get('status', 'new')
            
            # Active checkbox
            asset.active = request.POST.get('active') == 'on'
            
            # Date purchase
            date_purchase = request.POST.get('date_purchase')
            if date_purchase:
                asset.date_purchase = date_purchase
            
            # Remarks
            asset.remark = request.POST.get('remark', '')
            
            asset.save()
            return redirect('retail_asset_detail', id=asset.pk)
            
        except Exception as e:
            # If there's an error, re-render with error message
            return render(request, 'accounts/edit_retail_asset.html', {
                'asset': asset,
                'outlets': outlets,
                'statuses': RetailAsset.STATUS_CHOICES,
                'error': f'Error updating asset: {str(e)}'
            })
    
    context = {
        'asset': asset,
        'outlets': outlets,
        'statuses': RetailAsset.STATUS_CHOICES,
    }
    return render(request, 'accounts/edit_retail_asset.html', context)


# ============================================
# IT Assets Views
# ============================================

@login_required
def it_assets(request):
    assets = ITAsset.objects.all().select_related('outlet')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    outlet_filter = request.GET.get('outlet', '')
    asset_type_filter = request.GET.get('asset_type', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters
    if search_query:
        assets = assets.filter(
            Q(item__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(asset_id__icontains=search_query)
        )
    
    if outlet_filter:
        assets = assets.filter(outlet_id=outlet_filter)
    
    if asset_type_filter:
        assets = assets.filter(asset_type=asset_type_filter)
    
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    assets = assets.order_by('-date_purchase')
    
    # Get filter options
    outlets = Outlet.objects.all()
    asset_types = ITAsset.ITEM_TYPE_CHOICES
    statuses = ITAsset.STATUS_CHOICES
    
    return render(request, 'accounts/it_assets.html', {
        'assets': assets,
        'outlets': outlets,
        'asset_types': asset_types,
        'statuses': statuses,
        'search_query': search_query,
        'selected_outlet': outlet_filter,
        'selected_asset_type': asset_type_filter,
        'selected_status': status_filter,
    })


@login_required
def it_asset_detail(request, id):
    asset = get_object_or_404(ITAsset, id=id)
    return render(request, 'accounts/it_asset_detail.html', {'asset': asset})


@login_required
def add_it_asset(request):
    if request.method == 'POST':
        form = ITAssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            
            # If asset_id is empty, generate it
            if not asset.asset_id:
                asset.asset_id = ITAsset.generate_asset_id(asset.asset_type)
            
            asset.status = 'Active' if form.cleaned_data.get('active') else (asset.status or 'Draft')
            asset.save()
            return redirect('it_assets')
    else:
        form = ITAssetForm()
    return render(request, 'accounts/add_it_asset.html', {'form': form})


@login_required
def edit_it_asset(request, pk):
    """Edit an existing IT asset"""
    asset = get_object_or_404(ITAsset, pk=pk)
    outlets = Outlet.objects.all()
    
    if request.method == 'POST':
        try:
            # Get the outlet
            outlet_id = request.POST.get('outlet')
            outlet = get_object_or_404(Outlet, pk=outlet_id) if outlet_id else None
            
            # Update asset fields
            asset.asset_id = request.POST.get('asset_id', asset.asset_id)
            asset.asset_type = request.POST.get('asset_type', '')
            asset.item = request.POST.get('item', '')
            asset.brand = request.POST.get('brand', '')
            asset.model = request.POST.get('model', '')
            asset.serial_number = request.POST.get('serial_number', '')
            asset.allocation = request.POST.get('allocation', '')  # ← ADDED THIS LINE
            asset.outlet = outlet
            asset.status = request.POST.get('status', 'new')
            
            # Active checkbox
            asset.active = request.POST.get('active') == 'on'
            
            # Date purchase
            date_purchase = request.POST.get('date_purchase')
            if date_purchase:
                asset.date_purchase = date_purchase
            
            # Remarks
            asset.remarks = request.POST.get('remarks', '')
            
            asset.save()
            return redirect('it_asset_detail', id=asset.pk)
            
        except Exception as e:
            # If there's an error, re-render with error message
            return render(request, 'accounts/edit_it_asset.html', {
                'asset': asset,
                'outlets': outlets,
                'asset_types': ITAsset.ITEM_TYPE_CHOICES,
                'statuses': ITAsset.STATUS_CHOICES,
                'error': f'Error updating asset: {str(e)}'
            })
    
    context = {
        'asset': asset,
        'outlets': outlets,
        'asset_types': ITAsset.ITEM_TYPE_CHOICES,
        'statuses': ITAsset.STATUS_CHOICES,
    }
    return render(request, 'accounts/edit_it_asset.html', context)


# ============================================
# CPU Assets View
# ============================================

@login_required
def cpu_assets(request):
    outlets = Outlet.objects.all()
    selected_outlet = request.GET.get('outlet', None)
    quick_search = request.GET.get('quick_search', None)
    
    # Quick search - redirect to detail page
    if quick_search:
        try:
            asset = ITAsset.objects.filter(
                asset_type='cpu'
            ).filter(
                Q(serial_number__icontains=quick_search) |
                Q(item__icontains=quick_search) |
                Q(asset_id__icontains=quick_search)
            ).first()
            
            if asset:
                return redirect('it_asset_detail', id=asset.id)
        except Exception:
            pass
    
    # Filter CPU assets
    if selected_outlet:
        cpu_assets = ITAsset.objects.filter(
            asset_type='cpu',
            outlet_id=selected_outlet
        ).order_by('item')
    else:
        cpu_assets = ITAsset.objects.filter(asset_type='cpu').order_by('item')

    return render(request, 'accounts/cpu_assets.html', {
        'cpu_assets': cpu_assets,
        'outlets': outlets,
        'selected_outlet': selected_outlet
    })


# ============================================
# CCTV Assets View
# ============================================

@login_required
def cctv_assets(request):
    outlets = Outlet.objects.all()
    selected_outlet = request.GET.get('outlet', None)
    quick_search = request.GET.get('quick_search', None)
    
    # Quick search - redirect to detail page
    if quick_search:
        try:
            asset = ITAsset.objects.filter(
                asset_type='cctv'
            ).filter(
                Q(serial_number__icontains=quick_search) |
                Q(item__icontains=quick_search) |
                Q(asset_id__icontains=quick_search)
            ).first()
            
            if asset:
                return redirect('it_asset_detail', id=asset.id)
        except Exception:
            pass
    
    # Filter CCTV assets
    if selected_outlet:
        cctv_assets = ITAsset.objects.filter(
            asset_type='cctv',
            outlet_id=selected_outlet
        ).order_by('item')
    else:
        cctv_assets = ITAsset.objects.filter(asset_type='cctv').order_by('item')

    return render(request, 'accounts/cctv_assets.html', {
        'cctv_assets': cctv_assets,
        'outlets': outlets,
        'selected_outlet': selected_outlet
    })


# ============================================
# Network Assets Views
# ============================================

@login_required
def network_assets(request):
    assets = NetworkAsset.objects.all().select_related('outlet')
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    outlet_filter = request.GET.get('outlet', '')
    status_filter = request.GET.get('status', '')
    ip_filter = request.GET.get('ip', '')
    mac_filter = request.GET.get('mac', '')
    
    # Apply filters
    if search_query:
        assets = assets.filter(
            Q(item__icontains=search_query) |
            Q(sn__icontains=search_query) |
            Q(model__icontains=search_query)
        )
    
    if outlet_filter:
        assets = assets.filter(outlet_id=outlet_filter)
    
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    if ip_filter:
        assets = assets.filter(ip_address__icontains=ip_filter)
    
    if mac_filter:
        assets = assets.filter(mac_address__icontains=mac_filter)
    
    assets = assets.order_by('-date_purchase')
    
    # Get filter options
    outlets = Outlet.objects.all()
    statuses = NetworkAsset.STATUS_CHOICES
    
    return render(request, 'accounts/network_assets.html', {
        'assets': assets,
        'outlets': outlets,
        'statuses': statuses,
        'search_query': search_query,
        'selected_outlet': outlet_filter,
        'selected_status': status_filter,
        'ip_filter': ip_filter,
        'mac_filter': mac_filter,
    })


# ============================================
# Service Management Views
# ============================================

@login_required
def add_service(request, asset_id):
    asset = get_object_or_404(RetailAsset, id=asset_id)
    
    if request.method == 'POST':
        # Get form data from POST request
        service_date = request.POST.get('service_date')
        description = request.POST.get('description')
        technician = request.POST.get('technician') or None
        
        # Create service record
        Service.objects.create(
            asset=asset,
            service_date=service_date,
            description=description,
            technician=technician
        )
        
        return redirect('retail_asset_detail', id=asset.id)
    
    # If GET request, show the form
    form = ServiceForm()
    return render(request, 'accounts/add_service.html', {'form': form, 'asset': asset})


# ============================================
# Bulk Actions and Status Management
# ============================================

@login_required
def move_to_active(request, asset_id, asset_type):
    """Move an asset from Draft to Active status"""
    if asset_type == 'retail':
        asset = get_object_or_404(RetailAsset, id=asset_id)
    elif asset_type == 'it':
        asset = get_object_or_404(ITAsset, id=asset_id)
    else:
        return redirect('dashboard')
    
    if asset.status != 'Active':
        asset.status = 'Active'
        asset.active = True
        asset.save()
    
    # Redirect back to the appropriate list page
    if asset_type == 'retail':
        return redirect('retail_assets')
    elif asset_type == 'it':
        return redirect('it_assets')
    
    return redirect('dashboard')


@login_required
def bulk_action(request):
    """Handle bulk actions on multiple assets"""
    if request.method == 'POST':
        action = request.POST.get('action')
        asset_type = request.POST.get('asset_type')
        asset_ids = request.POST.getlist('asset_ids')
        
        if not action or not asset_ids:
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
        
        # Get the appropriate asset model
        if asset_type == 'retail':
            assets = RetailAsset.objects.filter(id__in=asset_ids)
        elif asset_type == 'it':
            assets = ITAsset.objects.filter(id__in=asset_ids)
        elif asset_type == 'network':
            assets = NetworkAsset.objects.filter(id__in=asset_ids)
        else:
            return redirect('dashboard')
        
        # Apply the action
        if action == 'activate':
            assets.update(status='Active', active=True)
        elif action == 'deactivate':
            assets.update(status='Inactive', active=False)
        elif action == 'maintenance':
            assets.update(status='Under Maintenance')
        
        # Redirect back to the referring page
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    return redirect('dashboard')