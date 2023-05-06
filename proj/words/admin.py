from django.contrib import admin

from .models import Word

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    ordering = ["word"]
    search_fields = ["word"]
    list_display = ["word", "was_answer", "familiarity"]