from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request=request,
                 template_name='basic_app/index.html',
                 )
@login_required# its work is simple it only you login before it can show you this page 
def dashboard(request):
    return HttpResponse( 'wellcome to your dashboard page')

@login_required
def user_logout(request):
    #This antomatically logout the user
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    # remenber why use the register False
    # this is used instant of the instance stuff
    registered = False


    # checking if is a Post reqeust
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if it is valid
        if user_form.is_valid() and profile_form.is_valid():

            #save the user_form first with an instance 
            user = user_form.save()
            
            # set a password sha
            user.set_password(user.password)

            # and save all
            user.save()

            # sending it to the database but not saving yet
            profile = profile_form.save(commit=False)

            #setting all the relationship
            profile.user = user

            # check for profile pic
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                # save everything
                profile.save()

                registered = True
            else:
                print(user_form.errors, profile_form.errors)
    else:        
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request=request,
                template_name='basic_app/registration.html',
                context={'user_form':user_form,
                        'profile_form':profile_form,
                        'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # To authenticate
        user = authenticate(username=username, password=password)

        # check is an account is active
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                HttpResponse('Account not active')
        else:
            print('Someone tried to login and failed')
            print('username: {} and password {}'.format(username,password))

            return HttpResponse('invalid login')

    else:
        return render(request=request,
                        template_name='basic_app/login.html')
                        
