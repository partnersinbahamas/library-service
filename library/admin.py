from django.contrib import admin

from library.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = (
        "id",
        "api_id",
        "title",
        "summaries",
        "author",
        "cover",
        "inventory",
        "daily_fee",
        "year_of_publication",
    )
    list_filter = (
        "cover",
        "year_of_publication",
    )
    search_fields = (
        "title",
        "author",
    )
    list_editable = ("cover", "inventory", "daily_fee")
    readonly_fields = ("id", "api_id", "year_of_publication")
