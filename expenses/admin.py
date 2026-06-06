from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "category", "regret_score", "created_at")
    list_filter = ("category",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
