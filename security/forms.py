from django import forms
from .models import Policy, Risk, PolicyVersion

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ["title", "content", "risks"]
        widgets = {
            'risks': forms.CheckboxSelectMultiple(),
        }

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ["name", "description", "severity"]

class PolicyVersionForm(forms.ModelForm):
    class Meta:
        model = PolicyVersion
        fields = ["notes"]