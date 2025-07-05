from django.contrib import admin
from .models import stuUser, Job, stuComp, UserProfile, Application, AppliedJob

admin.site.register(stuUser)
admin.site.register(stuComp)
admin.site.register(Job)
admin.site.register(UserProfile)
admin.site.register(Application)
admin.site.register(AppliedJob)
