from django.contrib import admin
from lecMgt_auth.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Department)
admin.site.register(Reasons)
admin.site.register(Leave)
admin.site.register(Qualification)
admin.site.register(Positions)
admin.site.register(LecturerProfile)
admin.site.register(Promotion)
