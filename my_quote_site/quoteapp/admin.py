from django.contrib import admin

from .models import Tag, Quotes, Autors

# Register your models here.

admin.site.register(Tag)
admin.site.register(Quotes)
admin.site.register(Autors)