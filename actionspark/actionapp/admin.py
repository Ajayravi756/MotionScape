from django.contrib import admin

# Register your models here.
from . models import Video,customertbl
admin.site.register(Video)
admin.site.register(customertbl)

