from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Profile
from gatepass_apply.models import Gatepass, Item
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import render_to_pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from manager.forms import ProfileUpdateForm
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q
from manager.forms import SignupForm
from django.contrib import messages

# Create your views here.


authorize_users = ["BH1 Supervisor", "BH2 Supervisor", "BH3 Supervisor", "GH Supervisor", "Control Room", "BH1 Warden", \
                   "BH2 Warden", "BH3 Warden", "GH Warden", "BH1 Assistant Warden", "BH2 Assistant Warden",
                   "BH3 Assistant Warden", \
                   "GH Assistant Warden", ]


@login_required
def index(request):
    if request.user.is_superuser:
        prof = Profile.objects.get(user=request.user)
        context = {'prof': prof}
        return redirect('manager:list_users')
    else:
        return HttpResponse("Permission Denied")


@login_required
def list_users(request):
    if request.user.is_superuser:
        users = Profile.objects.all().filter(user_type__in=authorize_users)
        prof = Profile.objects.get(user=request.user)
        context = {'prof': prof, 'users': users}
        return render(request, 'manager/list_user.html', context=context)
    else:
        return HttpResponse("Permission Denied")


@login_required
def update_user(request, id):
    if request.user.is_superuser:
        user = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        if request.method == "POST":
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                prof = form.save(commit=False)
                prof.user = get_object_or_404(User, id=request.POST['user'])
                prof.save()
                return redirect('index')
        else:
            form = ProfileUpdateForm(instance=user)
            prof = Profile.objects.get(user=request.user)
            context = {'form': form, 'prof': prof}
            return render(request, 'manager/update_user.html', context)
    else:
        return HttpResponse("Permission Denied")


@login_required
def user_detail(request, id):
    if request.user.is_superuser:
        userd = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        prof = Profile.objects.get(user=request.user)
        context = {'userd': userd, 'prof': prof}
        return render(request, 'manager/detail.html', context)
    else:
        return HttpResponse("Permission Denied")


@login_required
def del_user(request, id):
    if request.user.is_superuser:
        userd = get_object_or_404(User, id=id)
        userd.delete()
        return redirect('manager:index')
    else:
        return HttpResponse("Permission Denied")


@login_required
def pending_list(request):
    if request.user.is_superuser:
        prof = Profile.objects.get(user=request.user)
        pending_passes = Gatepass.objects.all().exclude(
            Q(hostel_warden="Rejected") | Q(hostel_assistant_warden="Rejected") \
            | Q(hostel_supervisor="Rejected") | Q(control_room="Rejected")).filter(Q(hostel_supervisor="Pending") | \
                                                                                   Q(hostel_warden="Pending") & Q(
            hostel_assistant_warden="Pending") | Q(control_room="Pending")).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(pending_passes, 10)
        try:
            pending_passes = paginator.page(page)
        except PageNotAnInteger:
            pending_passes = paginator.page(1)
        except EmptyPage:
            pending_passes = paginator.page(paginator.num_pages)
        context = {'prof': prof, 'pending_passes': pending_passes}
        return render(request, 'manager/pending_list.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def rejected_list(request):
    if request.user.is_superuser:
        prof = Profile.objects.get(user=request.user)
        rejected_passes = Gatepass.objects.all().filter(
            Q(hostel_supervisor="Rejected") | Q(hostel_warden="Rejected") | Q(hostel_assistant_warden="Rejected") | Q(
                control_room="Rejected")).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(rejected_passes, 10)
        try:
            rejected_passes = paginator.page(page)
        except PageNotAnInteger:
            rejected_passes = paginator.page(1)
        except EmptyPage:
            rejected_passes = paginator.page(paginator.num_pages)
        context = {'prof': prof, 'rejected_passes': rejected_passes}
        return render(request, 'manager/rejected_list.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def approved_list(request):
    if request.user.is_superuser:
        prof = Profile.objects.get(user=request.user)
        approved_passes = Gatepass.objects.all().exclude(
            Q(hostel_warden="Rejected") | Q(hostel_assistant_warden="Rejected")).filter(
            Q(hostel_supervisor="Approved") & (Q(hostel_warden="Approved") | Q(hostel_assistant_warden="Approved")) & Q(
                control_room="Approved")).order_by('-id')

        page = request.GET.get('page', 1)
        paginator = Paginator(approved_passes, 10)
        try:
            approved_passes = paginator.page(page)
        except PageNotAnInteger:
            approved_passes = paginator.page(1)
        except EmptyPage:
            approved_passes = paginator.page(paginator.num_pages)
        context = {'prof': prof, 'approved_passes': approved_passes}
        return render(request, 'manager/approved_list.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def add_user(request):
    if request.user.is_superuser:
        prof = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form = SignupForm(request.POST)
            extendForm = ProfileUpdateForm(request.POST)
            var = "xxx"
            try:
                var = User.objects.all().get(username=request.POST.get('username'))
            except:
                var = "xxx"
            print(var)
            if var != "xxx":
                if User.objects.all().get(username=request.POST.get('username')).is_active:
                    messages.warning(request, 'Account already exist with this username!')
                    return redirect('manager:add_user')
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                profile = Profile(user=user)
                profile.first_name = request.POST['first_name']
                profile.last_name = request.POST['last_name']
                profile.user_type = request.POST['user_type']
                profile.email_id = request.POST['email_id']
                profile.mob_no = request.POST['mob_no']
                profile.save()
                return redirect('manager:list_users')
        else:
            form = SignupForm()
            extendForm = ProfileUpdateForm()
            return render(request, 'manager/signup.html', {'form': form, 'extendForm': extendForm, 'prof': prof})
    else:
        return render(request, 'permission_denied.html', context=context)


@login_required
def gatepass_detail(request, id):
    if request.user.is_superuser:
        pass_detail = Gatepass.objects.all().get(id=id)
        prof = Profile.objects.get(user=request.user)
        items = Item.objects.all().filter(gatepass=pass_detail)
        context = {'gatepass': pass_detail, 'items': items, 'prof': prof, 'type': prof.user_type}
        return render(request, 'manager/gatepass_detail.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)
