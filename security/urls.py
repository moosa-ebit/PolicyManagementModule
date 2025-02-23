from django.urls import path
from . import views

urlpatterns = [
    path('create-policy', views.create_policy, name='create_policy'),
    path('edit-policy/<int:pk>', views.edit_policy, name='edit_policy'),
    path('policy-list', views.view_policies, name='view_policies'),
    path('create-risk', views.create_risk, name='create_risk'),
    path('edit-risk/<int:pk>', views.edit_risk, name='edit_risk'),
    path('risk-list', views.view_risks, name='view_risks'),
    path('create-compliance-standard', views.create_compliance_standard, name='create_compliance_standard'),
    path('edit-compliance-standard/<int:pk>', views.edit_compliance_standard, name='edit_compliance_standard'),
    path('compliance-standard-list', views.view_compliance_standard, name='view_compliance_standard'),
    path('policy/<int:pk>/policy-version-list', views.view_policy_versions, name='view_policy_versions'),
    path('view-policy-version/<int:pk>', views.view_policy_version, name='view_policy_version'),
    path('edit-policy-version/<int:pk>', views.edit_policy_version, name='edit_policy_version'),
    path('rollback-policy-version/<int:pk>', views.rollback_policy_version, name='rollback_policy_version'),
    path('view-policy-acknowledgment', views.view_policy_acknowledgment, name='view_policy_acknowledgment'),
    path('view-policy/<int:pk>', views.view_policy, name='view_policy'),
    path('policy/<int:pk>/policy-acknowledgment-list', views.view_policy_acknowledgments, name='view_policy_acknowledgments'),
    path('download-ack-report/<int:pk>', views.download_ack_report, name='download_ack_report'),
    path('submit-policy/<int:pk>', views.submit_policy, name='submit_policy'),
    path('archive-policy/<int:pk>', views.archive_policy, name='archive_policy'),
]