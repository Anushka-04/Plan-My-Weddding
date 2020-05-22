from django.urls import path
from . import views
from .views import (
HomeView,VendorView, vendor_type_list,VendorDetailView,register, AddSummary, add_to_list,
)


app_name = "home"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('type/<str:type_name>/', views.vendor_type_list, name='type'),
    path('vendors/', VendorView.as_view(), name='vendors'),
    path('vendor/<slug>', VendorDetailView.as_view(), name='vendor'),
    path('signup/', views.register, name='signup'),
    path("adds/", AddSummary.as_view(), name="adds"),
    path("add-to-list/<slug>/", add_to_list, name="add-to-list"),


    ]