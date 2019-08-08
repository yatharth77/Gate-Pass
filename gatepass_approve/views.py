from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Profile
from gatepass_apply.models import Gatepass, Item
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import render_to_pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

authorize_users = ["BH1 Supervisor", "BH2 Supervisor", "BH3 Supervisor", "GH Supervisor", "Control Room", "BH1 Warden", \
                   "BH2 Warden", "BH3 Warden", "GH Warden", "BH1 Assistant Warden", "BH2 Assistant Warden",
                   "BH3 Assistant Warden", \
                   "GH Assistant Warden"]


@login_required
def index(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        if prof.user_type in authorize_users:
            return redirect('gatepass_approve:pending_list')
        # context={'prof':prof}
        # return render(request,'base.html',context=context)
        else:
            context = {'prof': prof}
            return render(request, 'permission_denied.html', context=context)


def pending_list(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        if prof.user_type in authorize_users:
            pending_passes = Gatepass.objects.all()
            if prof.user_type == "BH1 Supervisor":
                pending_passes = Gatepass.objects.all().filter(hostel_supervisor="Pending").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_warden="Pending").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Assistant Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Pending").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH2 Supervisor":
                pending_passes = Gatepass.objects.all().filter(hostel_supervisor="Pending").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_warden="Pending").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Assistant Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Pending").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH3 Supervisor":
                pending_passes = Gatepass.objects.all().filter(hostel_supervisor="Pending").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_warden="Pending").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Assistant Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Pending").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "GH Supervisor":
                pending_passes = Gatepass.objects.all().filter(hostel_supervisor="Pending").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_warden="Pending").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Assistant Warden":
                pending_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Pending").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "Control Room":
                pending_passes = Gatepass.objects.all().filter(control_room="Pending")

            pending_passes = pending_passes.order_by('-id')
            page = request.GET.get('page', 1)
            paginator = Paginator(pending_passes, 10)
            try:
                pending_passes = paginator.page(page)
            except PageNotAnInteger:
                pending_passes = paginator.page(1)
            except EmptyPage:
                pending_passes = paginator.page(paginator.num_pages)
            context = {'prof': prof, 'pending_passes': pending_passes}
            return render(request, 'gatepass_approve/pending_list.html', context=context)
        else:
            context = {'prof': prof}
            return render(request, 'permission_denied.html', context=context)


def approved_list(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        if prof.user_type in authorize_users:
            approved_passes = Gatepass.objects.all()
            if prof.user_type == "BH1 Supervisor":
                approved_passes = Gatepass.objects.all().filter(hostel_supervisor="Approved").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_warden="Approved").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Assistant Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Approved").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH2 Supervisor":
                approved_passes = Gatepass.objects.all().filter(hostel_supervisor="Approved").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_warden="Approved").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Assistant Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Approved").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH3 Supervisor":
                approved_passes = Gatepass.objects.all().filter(hostel_supervisor="Approved").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_warden="Approved").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Assistant Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Approved").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "GH Supervisor":
                approved_passes = Gatepass.objects.all().filter(hostel_supervisor="Approved").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_warden="Approved").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Assistant Warden":
                approved_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Approved").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "Control Room":
                approved_passes = Gatepass.objects.all().filter(control_room="Approved")
            approved_passes = approved_passes.order_by('-id')
            page = request.GET.get('page', 1)
            paginator = Paginator(approved_passes, 10)
            try:
                approved_passes = paginator.page(page)
            except PageNotAnInteger:
                approved_passes = paginator.page(1)
            except EmptyPage:
                approved_passes = paginator.page(paginator.num_pages)
            context = {'prof': prof, 'approved_passes': approved_passes}
            return render(request, 'gatepass_approve/approved_list.html', context=context)
        else:
            context = {'prof': prof}
            return render(request, 'permission_denied.html', context=context)


def rejected_list(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        if prof.user_type in authorize_users:
            rejected_passes = Gatepass.objects.all()
            if prof.user_type == "BH1 Supervisor":
                rejected_passes = Gatepass.objects.all().filter(hostel_supervisor="Rejected").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_warden="Rejected").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH1 Assistant Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Rejected").filter(
                    hostel="BH1(Arawali Hostel)")
            elif prof.user_type == "BH2 Supervisor":
                rejected_passes = Gatepass.objects.all().filter(hostel_supervisor="Rejected").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_warden="Rejected").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH2 Assistant Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Rejected").filter(
                    hostel="BH2(Nilgiri Hostel)")
            elif prof.user_type == "BH3 Supervisor":
                rejected_passes = Gatepass.objects.all().filter(hostel_supervisor="Rejected").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_warden="Rejected").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "BH3 Assistant Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Rejected").filter(
                    hostel="BH3(Shivalik Hostel)")
            elif prof.user_type == "GH Supervisor":
                rejected_passes = Gatepass.objects.all().filter(hostel_supervisor="Rejected").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_warden="Rejected").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "GH Assistant Warden":
                rejected_passes = Gatepass.objects.all().filter(hostel_assistant_warden="Rejected").filter(
                    hostel="GH(Gangotri Hostel)")
            elif prof.user_type == "Control Room":
                rejected_passes = Gatepass.objects.all().filter(control_room="Rejected")
            rejected_passes = rejected_passes.order_by('-id')
            page = request.GET.get('page', 1)
            paginator = Paginator(rejected_passes, 10)
            try:
                rejected_passes = paginator.page(page)
            except PageNotAnInteger:
                rejected_passes = paginator.page(1)
            except EmptyPage:
                rejected_passes = paginator.page(paginator.num_pages)
            context = {'prof': prof, 'rejected_passes': rejected_passes}
            return render(request, 'gatepass_approve/rejected_list.html', context=context)
        else:
            context = {'prof': prof}
            return render(request, 'permission_denied.html', context=context)


def gatepass_detail(request, id):
    pass_detail = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.get(user=request.user)
    items = Item.objects.all().filter(gatepass=pass_detail)
    if pass_detail.hostel == "BH1(Arawali Hostel)" and (
            prof.user_type in ["BH1 Supervisor", "BH1 Warden", "BH1 Assistant Warden"]) \
            or pass_detail.hostel == "BH2(Nilgiri Hostel)" and (
            prof.user_type in ["BH2 Supervisor", "BH2 Warden", "BH2 Assistant Warden"]) \
            or pass_detail.hostel == "BH3(Shivalik Hostel)" and (
            prof.user_type in ["BH3 Supervisor", "BH3 Warden", "BH3 Assistant Warden"]) \
            or pass_detail.hostel == "GH(Gangotri Hostel)" and (
            prof.user_type in ["GH Supervisor", "GH Warden", "GH Assistant Warden"]) \
            or prof.user_type == "Control Room":
        context = {'gatepass': pass_detail, 'items': items, 'prof': prof, 'type': prof.user_type}
        return render(request, 'gatepass_approve/gatepass_detail.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def approve_gatepass_hostel_supervisor(request, id):
    gatepass = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.all().get(user=request.user)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Supervisor" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Supervisor" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Supervisor" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Supervisor":
        gatepass.hostel_supervisor = "Approved"
        gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def approve_gatepass_hostel_warden(request, id):
    gatepass = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.all().get(user=request.user)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Warden" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Warden" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Warden" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Warden":
        gatepass.hostel_warden = "Approved"
        gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def approve_gatepass_hostel_assistant_warden(request, id):
    gatepass = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.all().get(user=request.user)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Assistant Warden" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Assistant Warden" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Assistant Warden" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Assistant Warden":
        gatepass.hostel_assistant_warden = "Approved"
        gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def approve_gatepass_control_room(request, id):
    gatepass = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.all().get(user=request.user)
    if prof.user_type == "Control Room":
        gatepass.control_room = "Approved"
        gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def reject_gatepass_control_room(request, id):
    prof = Profile.objects.all().get(user=request.user)
    if prof.user_type == "Control Room":
        if request.method == "POST":
            gatepass = Gatepass.objects.all().get(id=id)
            gatepass.control_room = "Rejected"
            gatepass.control_room_remark = request.POST.get('remark')
            gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def reject_gatepass_hostel_supervisor(request, id):
    prof = Profile.objects.all().get(user=request.user)
    gatepass = Gatepass.objects.all().get(id=id)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Supervisor" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Supervisor" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Supervisor" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Supervisor":
        if request.method == "POST":
            gatepass.hostel_supervisor = "Rejected"
            print(gatepass.hostel_supervisor)
            gatepass.hostel_supervisor_remark = request.POST.get('remark')
            gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def reject_gatepass_hostel_warden(request, id):
    prof = Profile.objects.all().get(user=request.user)
    gatepass = Gatepass.objects.all().get(id=id)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Warden" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Warden" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Warden" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Warden":
        if request.method == "POST":
            gatepass.hostel_warden = "Rejected"
            gatepass.hostel_warden_remark = request.POST.get('remark')
            gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def reject_gatepass_hostel_assistant_warden(request, id):
    prof = Profile.objects.all().get(user=request.user)
    gatepass = Gatepass.objects.all().get(id=id)
    if gatepass.hostel == "BH1(Arawali Hostel)" and prof.user_type == "BH1 Assistant Warden" \
            or gatepass.hostel == "BH2(Nilgiri Hostel)" and prof.user_type == "BH2 Assistant Warden" \
            or gatepass.hostel == "BH3(Shivalik Hostel)" and prof.user_type == "BH3 Assistant Warden" \
            or gatepass.hostel == "GH(Gangotri Hostel)" and prof.user_type == "GH Assistant Warden":
        if request.method == "POST":
            gatepass.hostel_assistant_warden = "Rejected"
            gatepass.hostel_assistant_warden_remark = request.POST.get('remark')
            gatepass.save()
        return redirect('gatepass_approve:pending_list')
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


class GeneratePdf(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        primary = self.kwargs['pk']
        gatepass = Gatepass.objects.all().get(pk=primary)
        items = Item.objects.all().filter(gatepass=gatepass)
        data = {'gatepass': gatepass, 'items': items}
        pdf = render_to_pdf('gatepass_approve/gatepass_print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
