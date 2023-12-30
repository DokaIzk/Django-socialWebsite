from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def dashboard(request):
    # displays' all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)

    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request, 'account/dashboard.html', {'section':'dashboard', 'actions':actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            newUser = user_form.save(commit=False)

            # set_password() handles password hashing before saving to the database
            newUser.set_password(
                user_form.cleaned_data['password']
            )

            newUser.save()

            Profile.objects.create(user=newUser)

            create_action(newUser, 'Has Created An Account')
            
            return render(request, 'account/register_done.html', {'newUser':newUser})
    
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'user_form':user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(instance=request.user, data=request.POST)
        profile_edit_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )

        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            messages.success(request, 'Profile Updated Successfully')
        
        else:
            messages.error(request, 'Error Updating Profile')

    else:
        user_edit_form = UserEditForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {
        'user_edit_form':user_edit_form,
        'profile_edit_form':profile_edit_form
    }) 

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)

    return render(request, 'account/user/list.html', {'section':'people', 'users':users}
)


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    # user_with_followers = User.objects.prefetch_related('followers').get(username=username, is_active=True)

    return render(request, 'account/user/detail.html', {'section':'people', 'user':user})


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')     

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)

            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)

                create_action(request.user, 'Followed', user)

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()

            return JsonResponse({'status': 'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
            
    return JsonResponse({'status': 'error'})
