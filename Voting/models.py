from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

RESIDENCY_CHOICES = [
    ('R', 'Resident'),
    ('NR', 'Non-Resident'),
]

GENDER_ALLOWED_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('B', 'Both'),
]

RESIDENCY_REQ_CHOICES = [
    ('All', 'All'),
    ('R', 'Resident'),
    ('NR', 'Non-Resident'),
]

class School(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=100)
    gender_allowed = models.CharField(max_length=1, choices=GENDER_ALLOWED_CHOICES, default='B')

    def __str__(self):
        return f"{self.name} ({self.get_gender_allowed_display()})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    residency_status = models.CharField(max_length=2, choices=RESIDENCY_CHOICES, default='NR')
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.school.name}"        

class Position(models.Model):
    title = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)  # Null for general positions
    residency_requirement = models.CharField(max_length=3, choices=RESIDENCY_REQ_CHOICES, default='All')
    gender_requirement = models.CharField(max_length=1, choices=GENDER_ALLOWED_CHOICES, default='B')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):
        desc = self.title
        if self.school:
            desc += f" ({self.school.name})"
        if self.hall:
            desc += f" ({self.hall.name})"
        return desc

class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.position.title}({self.school.name})"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.user.username}"
    
    class Meta:
        unique_together = ('voter', 'candidate')  # Ensure a voter can only vote for a candidate once

from django.core.validators import RegexValidator
username_validator = RegexValidator(
    regex=r'^[\w.@+\-/]+$',
    message='Enter a valid registration number. This value may contain only letters, numbers, and @/./+/-/_/ slashes characters.',
)
User._meta.get_field('username').validators = [username_validator]
