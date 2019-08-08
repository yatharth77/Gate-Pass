from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordContextMixin
from django.contrib.auth import update_session_auth_hash
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from accounts.forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from accounts.forms import ProfileUpdateForm
from accounts.models import Profile

app_name = 'accounts'


# Create your views here.
def index(request):
    context = {}
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        context = {'prof': prof}
        if request.user.is_superuser:
            return redirect('manager:index')
        if prof.user_type != "Student":
            return redirect('gatepass_approve:index')
        if prof.user_type == "Student":
            return redirect('gatepass_apply:apply')
    else:
        return render(request, 'base.html', context={})


@login_required
def view_profile(request):
    prof = Profile.objects.get(user=request.user)
    if prof.user_type == "Admin":
        return render(request, 'manager/view_profile.html', context={'prof': prof})
    else:
        return render(request, 'accounts/view_profile.html', context={'prof': prof})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Account is inactive!')
                return redirect('accounts:user_login')
        else:
            messages.warning(request, 'Incorrect password or username! ')
            return redirect('accounts:user_login')
    return render(request, 'registration/login.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if not request.POST.get('email').endswith('@iiitm.ac.in'):
            messages.warning(request, 'Use your webmail only!')
            form = SignupForm()
            return render(request, 'registration/signup.html', {'form': form})

        var = "xxx"
        try:
            var = User.objects.all().get(username=request.POST.get('username'))
        except:
            var = "xxx"
        print(var)
        if var != "xxx":
            if User.objects.all().get(username=request.POST.get('username')).is_active:
                messages.warning(request, 'Account already exist with this username! u can login')
                return redirect('accounts:user_login')
            else:
                messages.warning(request, 'Account is not active!')
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': var,
                    'domain': current_site.domain,
                    # .decode() after uid
                    'uid': urlsafe_base64_encode(force_bytes(var.pk)),  # .decode(),
                    'token': account_activation_token.make_token(var),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'registration/confirm_mail.html', {})
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            if User.objects.all().filter(email=request.POST.get('email')):
                messages.warning(request, 'Webmail already in use!')
                return render(request, 'registration/signup.html', {'form': form})
            user.save()
            profile = Profile(user=user)
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # .decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/confirm_mail.html', {})
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/mail_confirmed.html', {})
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def update_profile(request):
    user = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        print(request.POST['first_name'])
        print(request.POST['last_name'])
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = request.user
            prof.save()
            return redirect('index')
        else:
            print("Invalid form=================")

    else:
        form = ProfileUpdateForm(instance=user)
        prof = Profile.objects.get(user=request.user)
        context = {'form': form, 'prof': prof}
        return render(request, 'accounts/update_profile.html', context)


@login_required
def contact(request):
    prof = Profile.objects.get(user=request.user)
    # //mention suprvisor
    if prof.user_type == "Student":
        supervisor = Profile.objects.get(user=request.user)
        warden = Profile.objects.get(user=request.user)
        assistant_warden = Profile.objects.get(user=request.user)
        control_room = Profile.objects.get(user=request.user)
        if prof.hostel == "BH1(Arawali Hostel)":
            supervisor = Profile.objects.get(user_type="BH1 Supervisor")
            warden = Profile.objects.get(user_type="BH1 Warden")
            assistant_warden = Profile.objects.get(user_type="BH1 Assistant Warden")
            control_room = Profile.objects.get(user_type="Control Room")
        if prof.hostel == "BH2(Nilgiri Hostel)":
            supervisor = Profile.objects.get(user_type="BH2 Supervisor")
            warden = Profile.objects.get(user_type="BH2 Warden")
            assistant_warden = Profile.objects.get(user_type="BH2 Assistant Warden")
            control_room = Profile.objects.get(user_type="Control Room")
        if prof.hostel == "BH3(Shivalik Hostel)":
            supervisor = Profile.objects.get(user_type="BH3 Supervisor")
            warden = Profile.objects.get(user_type="BH3 Warden")
            assistant_warden = Profile.objects.get(user_type="BH3 Assistant Warden")
            control_room = Profile.objects.get(user_type="Control Room")
        if prof.hostel == "GH(Gangotri Hostel)":
            supervisor = Profile.objects.get(user_type="GH Supervisor")
            warden = Profile.objects.get(user_type="GH Warden")
            assistant_warden = Profile.objects.get(user_type="GH Assistant Warden")
            control_room = Profile.objects.get(user_type="Control Room")

        context = {'prof': prof, 'supervisor': supervisor, 'warden': warden, 'assistant_warden': assistant_warden,
                   'control_room': control_room}
        return render(request, 'accounts/contact.html', context=context)
    else:
        return render(request, 'permission_denied.html', {})


def contactUs(request):
    # //mention suprvisor
  #  if prof.user_type == "Student":
  #      supervisor = Profile.objects.get(user=request.user)
  #      warden = Profile.objects.get(user=request.user)
  #      assistant_warden = Profile.objects.get(user=request.user)
  #      control_room = Profile.objects.get(user=request.user)

    supervisor = []
    warden = []
    assistant_warden = []

    supervisor.append(Profile.objects.get(user_type="GH Supervisor"))
    warden.append(Profile.objects.get(user_type="GH Warden"))
    assistant_warden.append(Profile.objects.get(user_type="GH Assistant Warden"))
   # control_room.append(Profile.objects.get(user_type="Control Room"))
    
    supervisor.append(Profile.objects.get(user_type="BH1 Supervisor"))
    warden.append(Profile.objects.get(user_type="BH1 Warden"))
    assistant_warden.append(Profile.objects.get(user_type="BH1 Assistant Warden"))
   # control_room.append(Profile.objects.get(user_type="Control Room"))
  
    supervisor.append(Profile.objects.get(user_type="BH2 Supervisor"))
    warden.append(Profile.objects.get(user_type="BH2 Warden"))
    assistant_warden.append(Profile.objects.get(user_type="BH2 Assistant Warden"))
   # control_room.append(Profile.objects.get(user_type="Control Room"))

    supervisor.append(Profile.objects.get(user_type="BH3 Supervisor"))
    warden.append(Profile.objects.get(user_type="BH3 Warden"))
    assistant_warden.append(Profile.objects.get(user_type="BH3 Assistant Warden"))
    control_room = Profile.objects.get(user_type="Control Room")
    admin = Profile.objects.get(user_type="Admin")

    zip_list = zip(supervisor, warden , assistant_warden)

    context = {'control_room': control_room, 'admin':admin, 'zip_list' : zip_list}
    return render(request, 'accounts/contactUs.html', context=context)



class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prof = Profile.objects.all().get(user=self.request.user)
        context["prof"] = prof
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prof = Profile.objects.all().get(user=self.request.user)
        context["prof"] = prof
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
