from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    # ============================================
    # Default redirect from /accounts/ to /accounts/dashboard/
    # ============================================
    path('', RedirectView.as_view(url='dashboard/', permanent=True)),

    # ============================================
    # Authentication URLs
    # ============================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register_user'),  # FIXED: Changed from 'register' to 'register_user'
    
    # ============================================
    # Dashboard
    # ============================================
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ============================================
    # Asset ID Generation API Endpoints
    # ============================================
    path('api/retail-asset-id/', views.get_next_retail_asset_id, name='api_retail_asset_id'),
    path('api/it-asset-id/', views.get_next_it_asset_id, name='api_it_asset_id'),
    
    # ============================================
    # Retail Assets URLs
    # ============================================
    path('retail-assets/', views.retail_assets, name='retail_assets'),
    path('retail-assets/add/', views.add_retail_asset, name='add_retail_asset'),
    path('retail-assets/<int:id>/', views.retail_asset_detail, name='retail_asset_detail'),
    path('retail-assets/<int:pk>/edit/', views.edit_retail_asset, name='edit_retail_asset'),
    
    # ============================================
    # IT Assets URLs
    # ============================================
    path('it-assets/', views.it_assets, name='it_assets'),
    path('it-assets/add/', views.add_it_asset, name='add_it_asset'),
    path('it-assets/<int:id>/', views.it_asset_detail, name='it_asset_detail'),
    path('it-assets/<int:pk>/edit/', views.edit_it_asset, name='edit_it_asset'),
    
    # ============================================
    # CPU & CCTV Assets URLs
    # ============================================
    path('cpu-assets/', views.cpu_assets, name='cpu_assets'),
    path('cctv-assets/', views.cctv_assets, name='cctv_assets'),
    
    # ============================================
    # Network Assets URLs
    # ============================================
    path('network-assets/', views.network_assets, name='network_assets'),
    
    # ============================================
    # Service Management URLs
    # ============================================
    path('service/add/<int:asset_id>/', views.add_service, name='add_service'),
    
    # ============================================
    # Bulk Actions URLs
    # ============================================
    path('move-to-active/<int:asset_id>/<str:asset_type>/', views.move_to_active, name='move_to_active'),
    path('bulk-action/', views.bulk_action, name='bulk_action'),
]
