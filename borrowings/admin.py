from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "borrow_date",
        "expected_return_date",
        "return_date",
    )
    list_filter = ("book", "user")
    readonly_fields = ("id",)
    search_fields = ("book__title", "user__name")
