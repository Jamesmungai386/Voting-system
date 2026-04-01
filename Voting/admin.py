from django.contrib import admin
from .models import School, Position, Candidate, Vote

admin.site.register(School)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)

