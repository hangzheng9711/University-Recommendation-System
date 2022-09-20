from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.trainingSet)
admin.site.register(models.line)
admin.site.register(models.yiFenYiDang)
admin.site.register(models.school)