from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Save)
