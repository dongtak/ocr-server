from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        'bNum',
        'title',
        'author',
        'createdAt',
    ]

    list_filter = [
        'createdAt',
    ]

    sortable_by = [
        'bNum',
        'title',
        'author',
        'createdAt',
    ]