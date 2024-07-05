from django.contrib import admin
from .models import Room,Messages

admin.site.register(Messages)
admin.site.register(Room)