from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.school.name}"        

class Position(models.Model):
    title = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)  # Null for general positions
   
    def __str__(self):
        if self.school:
            return f"{self.title} ({self.school.name})"
        return self.title

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
