from django.shortcuts import render,redirect
from .models import Position, Candidate, School, Vote, StudentProfile, Hall
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        school_id = request.POST.get('school')
        gender = request.POST.get('gender')
        residency_status = request.POST.get('residency_status')
        hall_id = request.POST.get('hall')

        if form.is_valid() and school_id and gender and residency_status:
            user = form.save()
            school = School.objects.get(id=school_id)
            
            hall = None
            if residency_status == 'R' and hall_id:
                hall = Hall.objects.get(id=hall_id)
                
            StudentProfile.objects.create(
                user=user, 
                school=school,
                gender=gender,
                residency_status=residency_status,
                hall=hall
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    schools = School.objects.all()
    halls = Hall.objects.all()
    return render(request, 'registration/signup.html', {'form': form, 'schools': schools, 'halls': halls})

def home_view(request):

        if request.user.is_authenticated:
            return redirect('vote')  
        return redirect('login')

@login_required
def vote_view(request):
    if request.user.is_superuser:
        return redirect('results')

    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        return redirect('results')

    user_school = profile.school

    if Vote.objects.filter(voter=request.user).exists():
        return redirect('results')

    from django.db.models import Q
    eligible_positions = Position.objects.filter(
        Q(school=user_school) | Q(school__isnull=True),
        Q(residency_requirement='All') | Q(residency_requirement=profile.residency_status),
        Q(gender_requirement='B') | Q(gender_requirement=profile.gender),
        Q(hall=profile.hall) | Q(hall__isnull=True)
    ).prefetch_related('candidate_set')

    if request.method == 'POST':
        for position in eligible_positions:
            candidate_id = request.POST.get(f'position_{position.id}')
            if candidate_id:
                try:
                    candidate = Candidate.objects.get(id=candidate_id)
                    if not Vote.objects.filter(voter=request.user, candidate__position=position).exists():
                        Vote.objects.create(voter=request.user, candidate=candidate)
                except Candidate.DoesNotExist:
                    pass
        return redirect('results')

    general_positions = []
    school_positions = []
    hall_positions = []
    non_resident_positions = []
    
    for pos in eligible_positions:
        if pos.hall:
            hall_positions.append(pos)
        elif pos.residency_requirement == 'NR':
            non_resident_positions.append(pos)
        elif pos.school:
            school_positions.append(pos)
        else:
            general_positions.append(pos)

    return render(request, 'Voting/vote.html', {
        'general_positions': general_positions,
        'school_positions': school_positions,
        'hall_positions': hall_positions,
        'non_resident_positions': non_resident_positions,
        'school': user_school,
        'hall': profile.hall
    })

@login_required
def results_view(request):
    schools = School.objects.all()
    all_results = []
    general_results = []
    hall_results = []
    non_resident_results = []

    all_positions = Position.objects.all()

    for position in all_positions:
        candidates = Candidate.objects.filter(position=position)
        results = [(c, Vote.objects.filter(candidate=c).count()) for c in candidates]
        
        data = {'position': position, 'results': results}
        
        if position.hall:
            hall_results.append(data)
        elif position.residency_requirement == 'NR':
            non_resident_results.append(data)
        elif position.school:
            pass # handled below
        else:
            general_results.append(data)

    for school in schools:
        positions = Position.objects.filter(school=school)
        school_data = []
        for position in positions:
            candidates = Candidate.objects.filter(position=position)
            results = [(c, Vote.objects.filter(candidate=c).count()) for c in candidates]
            school_data.append({'position': position, 'results': results})
        all_results.append({'school': school, 'results': school_data})

    return render(request, 'Voting/results.html', {
        'all_results': all_results, 
        'general_results': general_results,
        'hall_results': hall_results,
        'non_resident_results': non_resident_results
    })
