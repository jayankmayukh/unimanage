from django.urls import path 
  
# importing views from views..py 
from . import views
  
urlpatterns = [ 
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('view_accessed_assets/', views.view_accessed_assets),
    path('view_asset/<int:id>/', views.view_asset),
    path('view_asset_access_requests/', views.view_asset_access_requests),
    path('create_asset_access_request/', views.create_asset_access_request),
    path('delete_asset_request/', views.delete_asset_request),
    path('manage_assets_managed/', views.manage_assets_managed),
    path('edit_asset/<int:id>/', views.edit_asset),
    path('manage_asset_requests/', views.manage_asset_requests),
    path('act_on_request/<int:id>/', views.act_on_request),
    path('view_asset_acquire_requests/', views.view_asset_acquire_requests),
    path('create_asset_acquire_request/', views.create_asset_acquire_request),
    path('manage_university_assets/', views.manage_university_assets),
    path('add_physical_asset/', views.add_physical_asset),
    path('add_software_asset/', views.add_software_asset),
    path('manage_acquire_requests/', views.manage_acquire_requests),
    path('act_on_acquire/<int:id>/', views.act_on_acquire),
    path('manage_locations/', views.manage_locations),
    path('delete_location/', views.delete_location),
    path('add_location', views.add_location)
] 