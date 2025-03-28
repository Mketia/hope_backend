from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('user__first_name', 'user__last_name')
    search_fields = ('user__username', 'user__email')
    ordering = ('-user__last_name',)

