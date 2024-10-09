from django.contrib import admin
from .models import Bookmark, CustomUser

# Register your models here.
admin.site.register(Bookmark)
admin.site.register(CustomUser)