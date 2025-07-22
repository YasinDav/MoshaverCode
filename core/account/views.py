from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from .forms import ProfileForm, AuthenticationFormCaptcha, UserCreationFormCaptcha
from .models import Profile
from index.views import profile_complete_required

# @login_required(login_url=settings.LOGIN_REDIRECT_URL)
# def edit_profile_view(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             return HttpResponse('Something went wrong')
#     if request.method == 'GET' or request.method == 'POST':
#         user = request.user
#         user_profile = Profile.objects.get(user=user)
#         form = ProfileForm(instance=user_profile)
#         return render(request, 'edit-profile.html', {'form': form})
#     else:
#         return HttpResponse('Something went wrong')

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def edit_profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)

            profile.save()

            tags_string = form.cleaned_data.get('tags', '')
            tags_list = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
            profile.skills.set(tags_list)

            return redirect('profile')
        else:
            return HttpResponse(form.errors, status=400)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit-profile.html', {'form': form})

profile_complete_required
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def profile_view(request):
    user = request.user
    user_profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {'user_profile': user_profile})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login'))


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationFormCaptcha(request=request.POST, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if next_url := request.POST.get("next"):
                        return redirect(next_url)
                    else:
                        return redirect(reverse("index"))

                else:
                    messages.error(request, 'Invalid Username or Password')

            else:
                messages.error(request, 'Bad request. Refresh page and try again')
        else:
            form = AuthenticationFormCaptcha()

        context_login = {"form": form}
        if next_url := request.POST.get('next'):
            context_login["next"] = next_url

        return render(request, 'login.html', context_login)
    else:
        return redirect(reverse('profile'))


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationFormCaptcha(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                user = authenticate(request, username=user.uesrname, password=form.password2)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, 'cannot login automatically. please try manually')
                    url = reverse('login')
                    if next_url := request.POST.get('next'):
                        url += "?next=" + next_url
                    return redirect(url)

                if next_url := request.POST.get('next'):
                    return redirect(next_url)
                else:
                    return redirect(reverse('profile'))

            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            form = UserCreationFormCaptcha()

        context_signup = {"form": form}
        if next_url := request.POST.get('next'):
            context_signup["next"] = next_url

        return render(request, 'accounts/signup.html', context_signup)
    else:
        return redirect(reverse('profile'))


@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def change_password_view(request):
    errors = None
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():

            password = form.cleaned_data['new_password2']
            request.user.set_password(password)
            request.user.save()

            user = authenticate(request, username=request.user.username, password=password)
            if user is not None:
                login(request, user)
                # messages.success("Password changed successfully", request.user)
                return redirect(reverse("profile"))
            else:
                return redirect(reverse("login"))

        else:
            errors = form.errors

    form = PasswordChangeForm(user=request.user)
    context_change_password = {"form": form}
    if errors is not None:
        context_change_password["errors"] = errors
    return render(request, "changepw.html", context_change_password)
