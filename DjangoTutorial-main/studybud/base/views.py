from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, JobForm, ResumeForm, CustomUserEditForm, ProfilePictureForm
from .models import Job, Field, Message, UserProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Job, UserProfile

# Create your views here.


#rooms = [
 #   {'id':1, 'name':'Lets learn python!'},
 #   {'id':2, 'name':'Design with me'},
  #  {'id':3, 'name':'Frontend developers'},
#]



def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')




    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Use does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {'page' : page}
    return render(request, 'base/login_register.html', context)


@login_required
def apply_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        user_profile = request.user.userprofile

        # Add job to the user's applied jobs list (stored as a comma-separated string)
        if user_profile.jobs_applied:
            jobs_applied = user_profile.jobs_applied.split(',')
        else:
            jobs_applied = []

        if str(job.id) not in jobs_applied:
            jobs_applied.append(str(job.id))

        # Update the jobs_applied field
        user_profile.jobs_applied = ','.join(jobs_applied)
        user_profile.save()

        return JsonResponse({'success': True, 'message': 'Job applied successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


def logoutUser(request):
    logout(request)
    return redirect('home')
    
def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occured during registration')

    return render(request, 'base/login_register.html', {'form':form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    jobs = Job.objects.filter(Q(field__name__icontains=q) |
                                 Q(name__icontains=q) |
                                   Q(description__icontains=q) 
    )

    fields = Field.objects.all()
    job_count = jobs.count()
    job_messages = Message.objects.filter(Q(job__field__name__icontains=q))



    context = {'jobs': jobs, 'fields':fields, 
               'job_count':job_count, 'job_messages': job_messages}
    return render(request, 'base/home.html', context)

def job(request, pk):
    job = Job.objects.get(id=pk)
    job_messages = job.message_set.all()
    participants = job.participants.all()


    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            job=job,
            body=request.POST.get('body')
        )
        job.participants.add(request.user)
        return redirect('job', pk=job.id)


    context = {'job': job, 'job_messages':job_messages, 'participants':participants}
    return render(request, 'base/create_job.html', context)


@login_required
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    jobs = user.job_set.all()
    job_messages = user.message_set.all()
    fields = Field.objects.all()

    profile, created = UserProfile.objects.get_or_create(user=user)
    
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    if request.user == user:
        if request.method == 'POST':
            resume_form = ResumeForm(request.POST, request.FILES, instance=profile)
            if resume_form.is_valid():
                resume_form.save() 
                return redirect('user-profile', pk=user.id)  
        else:
            resume_form = ResumeForm(instance=profile)  
    else:
        resume_form = None

    context = {'user':user, 'jobs':jobs, 'job_messages':job_messages, 'fields':fields,           
               'email': email, 'first_name': first_name, 'last_name': last_name, 
               'resume_form': resume_form, 'profile': profile}

    return render(request, 'base/profile.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  
    else:
        profile_form = ProfilePictureForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    user_profile = user.userprofile
    
    if request.method == 'POST':
        user_form = CustomUserEditForm(request.POST, instance=user)
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
            return redirect('user-profile', pk=user.id)
    else:
        user_form = CustomUserEditForm(instance=user)
        profile_form = ProfilePictureForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
    }

    return render(request, 'base/edit_profile.html', context)



@login_required(login_url='login')
def createJob(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateJob(request, pk):
    job = Job.objects.get(id=pk)
    form = JobForm(instance=job)

    if request.user != job.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteJob(request, pk):
    job = Job.objects.get(id=pk)

    if request.user != job.host:
        return HttpResponse('You are not allowed here!!')
    

    if request.method == 'POST':
        job.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':job})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})