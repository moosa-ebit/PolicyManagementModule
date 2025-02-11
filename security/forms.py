from django import forms
from .models import Policy, Risk, PolicyVersion, ComplianceStandard

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ["title", "content", "risks", "compliance_standards"]
        widgets = {
            'risks': forms.CheckboxSelectMultiple(),
            'compliance_standards': forms.CheckboxSelectMultiple(),
        }

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ["name", "description", "severity"]

class ComplianceStandardForm(forms.ModelForm):
    class Meta:
        model = ComplianceStandard
        fields = ["name", "description", "reference_url"]

class PolicyVersionForm(forms.ModelForm):
    class Meta:
        model = PolicyVersion
        fields = ["notes"]