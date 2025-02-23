from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from model_utils import FieldTracker

# Create your models here.    
class ComplianceStandard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    reference_url = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Risk(models.Model):
    Severity_Levels = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    severity = models.CharField(max_length=100, choices=Severity_Levels, default="LOW")
    updated_at = models.DateTimeField(auto_now=True)
    tracker = FieldTracker()

    def __str__(self):
        return self.name
    
class Policy(models.Model):
    Status = [
        ("DRAFT", "Draft"),
        ("IN_REVIEW", "In Review"),
        ("APPROVED", "Approved"),
        ("ACTIVE", "Active"),
        ("ARCHIVED", "Archived"),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    status = models.CharField(max_length=25, choices=Status, default="DRAFT")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    risks = models.ManyToManyField(Risk)
    compliance_standards = models.ManyToManyField(ComplianceStandard)
    tracker = FieldTracker()
    version_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def submit(self):
        if self.status == "DRAFT": self.status = "IN_REVIEW"
        elif self.status == "IN_REVIEW": self.status = "APPROVED"
        else: self.status = "ACTIVE"
        self.save()
    
    def archive(self):
        self.status = "ARCHIVED"
        self.save()
    
class PolicyVersion(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    version_number = models.IntegerField(default=1)
    title = models.TextField(max_length=250)
    content = models.TextField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=250, default="")
    risks = models.ManyToManyField(Risk)
    compliance_standards = models.ManyToManyField(ComplianceStandard)

    def __str__(self):
        return self.policy.title + "-" + str(self.version_number) 
    
class PolicyAcknowledgment(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acknowledged_at = models.DateTimeField(auto_now_add=True)