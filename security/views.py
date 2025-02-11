from django.shortcuts import render, redirect
from .forms import PolicyForm, RiskForm, PolicyVersionForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Policy, Risk, PolicyVersion
from django.contrib import messages

# Create your views here.
@login_required(login_url="/login")
@permission_required(["security.view_policy", "security.delete_policy"], login_url="/access-denied")
def view_policies(request):
    policies = Policy.objects.all()
    
    if request.method == "POST":
        policy_id_delete = request.POST.get("policy-id-delete")
        policy_id_edit = request.POST.get("policy-id-edit")
        if policy_id_delete:
            policy = Policy.objects.filter(id=policy_id_delete).first()
            if policy:
                policy.delete()
                messages.success(request, "The policy was deleted successfully.")
        else:
            policy = Policy.objects.filter(id=policy_id_edit).first()
            return redirect("/edit-policy", pk=policy.id)


    return render(request, 'security/list_policy.html', {"policies": policies})

def create_policy_version(policy: Policy, request):
    new_policy_version = PolicyVersion(title = policy.title, content = policy.content, version_number = policy.version_count + 1, policy = policy, created_by = request.user)
    new_policy_version.save()
    related_risks = Risk.objects.filter(policy = policy.id)
    new_policy_version.risks.add(*related_risks)
    new_policy_version.save()
    policy.version_count = policy.version_count + 1
    policy.save()
    return new_policy_version

def check_policy_risks_changes(policy: Policy, related_risks_ids, request, policy_version):
    current_related_risks_ids = [risk.id for risk in policy.risks.all()]
    if (set(related_risks_ids) != set(current_related_risks_ids)):
        if policy_version == False:
            create_policy_version(policy, request)
            messages.success(request, "A new version of the policy has been created.")

        if policy_version:
            policy_version.risks.add(*policy.risks.all())

@login_required(login_url="/login")
@permission_required("security.add_policy", login_url="/access-denied")
def create_policy(request):
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.created_by = request.user
            policy.save()
            create_policy_version(policy, request)
            messages.success(request, "The policy was created successfully.")
            return redirect("/policy-list")
    else:
        form = PolicyForm()
    
    return render(request, 'security/create_policy.html', {"form": form})

@login_required(login_url="/login")
@permission_required("security.change_policy", login_url="/access-denied")
def edit_policy(request, pk):
    policy = Policy.objects.get(id=pk)
    policy_version = False
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            related_risks_ids = [risk.id for risk in Risk.objects.filter(policy = policy.id)]
            if policy.tracker.changed():
                policy_version = create_policy_version(policy, request)
                messages.success(request, "A new version of the policy has been created.")
                created_version = True
            form.save()
            check_policy_risks_changes(policy, related_risks_ids, request, policy_version)
            messages.success(request, "The policy was edited successfully.")
            return redirect("/policy-list")
    else:
        form = PolicyForm(instance=policy)
        context = {
            'form': form,
        }
    
    return render(request, 'security/edit_policy.html', {"form": form})

@login_required(login_url="/login")
@permission_required(["security.view_risk", "security.delete_risk"], login_url="/access-denied")
def view_risks(request):
    risks = Risk.objects.all()
    
    if request.method == "POST":
        risk_id_delete = request.POST.get("risk-id-delete")
        risk_id_edit = request.POST.get("risk-id-edit")
        if risk_id_delete:
            risk = Policy.objects.filter(id=risk_id_delete).first()
            if risk:
                risk.delete()
                messages.success(request, "The risk was deleted successfully.")
        else:
            risk = Policy.objects.filter(id=risk_id_edit).first()
            return redirect("/edit-risk", pk=risk.id)


    return render(request, 'security/list_risk.html', {"risks": risks})

@login_required(login_url="/login")
@permission_required("security.add_risk", login_url="/access-denied")
def create_risk(request):
    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.created_by = request.user
            risk.save()
            messages.success(request, "The risk was created successfully.")
            return redirect("/risk-list")
    else:
        form = RiskForm()
    
    return render(request, 'security/create_risk.html', {"form": form})

@login_required(login_url="/login")
@permission_required("security.change_risk", login_url="/access-denied")
def edit_risk(request, pk):
    risk = Risk.objects.get(id=pk)
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            messages.success(request, "The risk was edited successfully.")
            return redirect("/risk-list")
    else:
        form = RiskForm(instance=risk)
        context = {
            'form': form,
        }
    
    return render(request, 'security/edit_risk.html', {"form": form})

@login_required(login_url="/login")
@permission_required(["security.view_policyversion", "security.delete_policyversion"], login_url="/access-denied")
def view_policy_versions(request, pk):
    policy_versions = PolicyVersion.objects.filter(policy = pk).order_by('-created_at')

    if request.method == "POST":
        policy_version_id_view = request.POST.get("policy-version-id-view")
        policy_version_id_delete = request.POST.get("policy-version-id-delete")
        if policy_version_id_delete:
            policy_version = PolicyVersion.objects.filter(id=policy_version_id_delete).first()
            if policy_version:
                policy_version.delete()
                messages.success(request, "The policy version was deleted successfully.")
        else:
            policy_version = Policy.objects.filter(id=policy_version_id_view).first()
            return redirect("/view-policy-version", pk=policy_version.id)


    return render(request, 'security/list_policy_version.html', {"policy_versions": policy_versions})

@login_required(login_url="/login")
@permission_required("security.view_policyversion", login_url="/access-denied")
def view_policy_version(request, pk):
    policy_version = PolicyVersion.objects.get(id=pk)
    # form = PolicyVersionForm(request.POST, instance=policy_version)
    return render(request, 'security/view_policy_version.html', {"policy_version": policy_version})

@login_required(login_url="/login")
@permission_required("security.change_policyversion", login_url="/access-denied")
def edit_policy_version(request, pk):
    policy_version = PolicyVersion.objects.get(id=pk)
    if request.method == 'POST':
        form = PolicyVersionForm(request.POST, instance=policy_version)
        if form.is_valid():
            form.save()
            messages.success(request, "The policy version was edited successfully.")
            return redirect("view_policy_versions", pk=policy_version.policy.id)
    else:
        form = PolicyVersionForm(instance=policy_version)
        context = {
            'form': form,
        }
    
    return render(request, 'security/edit_policy_version.html', {"form": form})