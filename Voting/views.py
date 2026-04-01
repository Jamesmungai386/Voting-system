from django.shortcuts import render,redirect
from .models import  Position, Candidate, School, Vote, StudentProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        school_id = request.POST.get('school')
        if form.is_valid():
            user = form.save()

            school = School.objects.get(id=school_id)
            StudentProfile.objects.create(user=user, school=school)
            return redirect('login')
    else:
        form = UserCreationForm()
        schools = School.objects.all()

    return render(request, 'registration/signup.html', {'form': form, 'schools': schools})

def home_view(request):

        if request.user.is_authenticated:
            return redirect('vote')  
        return redirect('login')

@login_required
def vote_view(request):

    user_school = request.user.studentprofile.school

    if Vote.objects.filter(voter = request.user).exists():
        return redirect('results')

    schools = School.objects.filter(name=user_school.name).prefetch_related('position_set__candidate_set')
    general_positions = Position.objects.filter(school__isnull=True).prefetch_related('candidate_set')
    if request.method == 'POST':

        for position in general_positions:
            candidate_id = request.POST.get(f'position_{position.id}')
            if candidate_id:
                candidate = Candidate.objects.get(id=candidate_id)
                if not Vote.objects.filter(voter=request.user, candidate__position=position).exists():
                    Vote.objects.create(voter=request.user, candidate=candidate)

        for school in schools:
            for position in school.position_set.all():
                candidate_id = request.POST.get(f'position_{position.id}')
                if candidate_id:
                    candidate = Candidate.objects.get(id=candidate_id)
                    if not Vote.objects.filter(voter=request.user, candidate__position=position).exists():
                        Vote.objects.create(voter=request.user, candidate=candidate)
        return redirect('results')
    # Assuming you want to show candidates for all position
    return render(request, 'voting/vote.html', {'schools': schools, 'general_positions': general_positions})

@login_required
def results_view(request):
    schools = School.objects.all()
    all_results = []
    general_results = []

    general_positions = Position.objects.filter(school__isnull=True)

    for position in general_positions:
        candidates = Candidate.objects.filter(position=position)
        results = [(c, Vote.objects.filter(candidate=c).count()) for c in candidates]
        general_results.append({'position': position, 'results': results})

    for school in schools:
        positions = Position.objects.filter(school=school)
        school_data=[]

        for position in positions:
            candidates = Candidate.objects.filter(position=position)

            results = [(c, Vote.objects.filter(candidate=c).count()) for c in candidates]
            school_data.append({'position': position, 'results': results})
        all_results.append({'school': school, 'results': school_data})


  

    return render(request, 'Voting/results.html', {'all_results': all_results, 'general_results': general_results})
