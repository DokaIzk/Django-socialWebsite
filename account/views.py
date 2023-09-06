from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)    

#         if form.is_valid():
#             cleanData = form.cleaned_data

#             user = authenticate(request, 
#                                 username=cleanData['username'],
#                                 password=cleanData['password'])
            
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)

#                     return HttpResponse('Authentication Successful')
                
#                 else:
#                     return HttpResponse('Disabled Account')
                
#             else:
#                 return HttpResponse('Invalid Login')
            
#     else:
#         form = LoginForm()

#     return render(request, 'account/login.html', {'form':form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', 
                  {'section':'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            newUser = user_form.save(commit=False)

            newUser.set_password(
                user_form.cleaned_data['password']
            )

            newUser.save()

            Profile.objects.create(user=newUser)
            
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