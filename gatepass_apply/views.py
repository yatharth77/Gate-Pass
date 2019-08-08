from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gatepass_apply.forms import ApplyForm
from gatepass_apply.models import Gatepass, Item
from accounts.models import Profile
from django.core.files.base import ContentFile
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import render_to_pdf
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta


# Create your views here.
@login_required
def apply(request):
    prof = Profile.objects.all().get(user=request.user)
    if prof.user_type == "Student":
        if request.method == "POST":
            form = ApplyForm(request.POST)
            if form.is_valid():
                gatepass = form.save(commit=False)
                gatepass.user = request.user
                prof = Profile.objects.all().get(user=request.user)
                gatepass.first_name = prof.first_name
                gatepass.last_name = prof.last_name
                gatepass.roll_no = prof.roll_no
                gatepass.mob_no = prof.mob_no
                gatepass.room_no = prof.room_no
                gatepass.father_name = prof.father_name
                gatepass.father_mobile = prof.father_mobile
                gatepass.hostel = prof.hostel
                applied_on = request.POST['applied_on']
                ff = "%Y-%m-%d %H:%M:%S.%f"
                applied_on = datetime.strptime(str(applied_on), ff)
                if prof.pic:
                    gatepass.pic.save('pic.jpeg', prof.pic, save=False)
                gatepass.save()
                return redirect('gatepass_apply:add_item', gatepass.id)
        form = ApplyForm()
        prof = Profile.objects.get(user=request.user)
        context = {'form': form, 'prof': prof}
        return render(request, 'gatepass_apply/apply_form.html', context=context)
    else:
        prof = Profile.objects.all().get(user=request.user)
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def add_item(request, id):
    gatepass = Gatepass.objects.all().get(id=id)
    prof = Profile.objects.all().get(user=request.user)
    if gatepass.user == request.user and prof.user_type == "Student":
        if request.method == "POST":
            Item.objects.filter(gatepass=gatepass).delete()
            gatepass_id = request.POST['gatepass_id']
            count = int(request.POST['count'])
            for i in range(count):
                detail = str(i)
                quantity = str(i + 100)
                remark = str(i + 200)
                print("post req:", request.POST[detail])
                item = Item(gatepass=gatepass, detail=request.POST[detail], quantity=request.POST[quantity],
                            remark=request.POST[remark])
                item.save()
            return redirect('gatepass_apply:history')
        else:
            prof = Profile.objects.get(user=request.user)
            items = Item.objects.all().filter(gatepass=Gatepass.objects.get(id=id))
            context = {'prof': prof, 'items': items, 'id': id}
            return render(request, 'gatepass_apply/add_item.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def delete_item(request, id, gatepass_id):
    gatepass = Gatepass.objects.all().get(id=gatepass_id)
    prof = Profile.objects.all().get(user=request.user)
    item = Item.objects.all().get(id=id)
    if gatepass.user == request.user and prof.user_type == "Student":
        item.delete()
        return redirect('gatepass_apply:add_item', gatepass_id)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def history(request):
    prof = Profile.objects.all().get(user=request.user)
    if prof.user_type == "Student":
        obj = Gatepass.objects.all().filter(user=request.user).order_by('-id')
        prof = Profile.objects.get(user=request.user)

        page = request.GET.get('page', 1)
        paginator = Paginator(obj, 10)
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)
        context = {'gatepasses': obj, 'prof': prof}
        return render(request, 'gatepass_apply/history.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def gatepass_detail(request, id):
    prof = Profile.objects.all().get(user=request.user)
    pass_detail = Gatepass.objects.all().get(id=id)
    if pass_detail.user == request.user and prof.user_type == "Student":
        items = Item.objects.all().filter(gatepass=pass_detail)
        prof = Profile.objects.get(user=request.user)
        context = {'gatepass': pass_detail, 'items': items, 'prof': prof}
        return render(request, 'gatepass_apply/gatepass_detail.html', context=context)
    else:
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def gatepass_delete(request, id):
    pas = Gatepass.objects.all().get(id=id)
    if pas.user == request.user:
        pas.delete()
        return redirect('gatepass_apply:history')
    else:
        prof = Profile.objects.all().get(user=request.user)
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


@login_required
def gatepass_update(request, id):
    instance = Gatepass.objects.all().get(id=id)
    if instance.user == request.user:
        if request.method == "POST":
            form = ApplyForm(request.POST, instance=instance)
            if form.is_valid():
                gatepass = form.save(commit=False)
                gatepass.user = request.user
                prof = Profile.objects.all().get(user=request.user)
                gatepass.first_name = prof.first_name
                gatepass.last_name = prof.last_name
                gatepass.roll_no = prof.roll_no
                gatepass.mob_no = prof.mob_no
                gatepass.room_no = prof.room_no
                gatepass.father_name = prof.father_name
                gatepass.father_mobile = prof.father_mobile
                gatepass.hostel = prof.hostel
                gatepass.save()
                return redirect('gatepass_apply:add_item', gatepass.id)
        form = ApplyForm(instance=instance)
        prof = Profile.objects.get(user=request.user)
        context = {'form': form, 'prof': prof}
        return render(request, 'gatepass_apply/apply_form.html', context=context)
    else:
        prof = Profile.objects.all().get(user=request.user)
        context = {'prof': prof}
        return render(request, 'permission_denied.html', context=context)


class GeneratePdf(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        primary = self.kwargs['pk']
        gatepass = Gatepass.objects.all().get(pk=primary)
        items = Item.objects.all().filter(gatepass=gatepass)
        data = {'gatepass': gatepass, 'items': items}
        pdf = render_to_pdf('gatepass_apply/gatepass_print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
