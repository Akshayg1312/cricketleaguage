from django.contrib import admin

from .models import *

regModel = list()

regModel.append(Countries)
regModel.append(Teams)
regModel.append(PlayerProfile)
regModel.append(Venue)
regModel.append(MatchList)
regModel.append(MatchSummery)

for row in regModel:
    @admin.register(row)
    class UniversalAdmin(admin.ModelAdmin):
        def get_list_display(self, request):
            return [field.name for field in self.model._meta.concrete_fields]
