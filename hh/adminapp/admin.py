from django.contrib import admin
from mainapp.models import Roles, Users, City, Articles, UserProfile, UserEdu, UserJobHistory
from mainapp.models import CompanyProfile, Articles, Vacancy, Categories

admin.site.register(City)
admin.site.register(Roles)
admin.site.register(Users)
admin.site.register(UserProfile)
admin.site.register(UserEdu)
admin.site.register(UserJobHistory)
admin.site.register(CompanyProfile)
admin.site.register(Articles)
admin.site.register(Categories)
admin.site.register(Vacancy)
