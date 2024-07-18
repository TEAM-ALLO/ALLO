from django.contrib import admin
from .models import Recycle

@admin.register(Recycle)
class RecycleAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')
# Register your models here.
