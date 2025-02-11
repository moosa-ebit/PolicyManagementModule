from django.urls import path
from . import views

urlpatterns = [
    path('create-policy', views.create_policy, name='create_policy'),
    path('edit-policy/<int:pk>', views.edit_policy, name='edit_policy'),
    path('policy-list', views.view_policies, name='view_policies'),
    path('create-risk', views.create_risk, name='create_risk'),
    path('edit-risk/<int:pk>', views.edit_risk, name='edit_risk'),
    path('risk-list', views.view_risks, name='view_risks'),
    path('policy/<int:pk>/policy-version-list', views.view_policy_versions, name='view_policy_versions'),
    path('view-policy-version/<int:pk>', views.view_policy_version, name='view_policy_version'),
    path('edit-policy-version/<int:pk>', views.edit_policy_version, name='edit_policy_version'),
]