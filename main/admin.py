from django.contrib import admin
from .models import Category, Book, BookCopy


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['TITLE']


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Presentation", {"fields": ["TITLE", "AUTHOR", "DATE", "LANGUAGE", "DESCRIPTION", "CATEGORY"]}),
        ("Description", {"fields": ["PRICE"]}), #"COPIES", "STATUS"]}),
    ]
    list_display = ['TITLE', 'AUTHOR', 'LANGUAGE', 'COPIES', 'PRICE', 'STATUS']
    list_filter = ['AUTHOR', 'DATE', 'LANGUAGE', 'STATUS']


class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['get_title', 'get_author', 'get_language', 'LAST_BORROWER',
                    'CLASSIFICATION', 'STATUS']
    list_filter = ['BOOK__TITLE', 'BOOK__AUTHOR', 'BOOK__LANGUAGE', 'LAST_BORROWER', 'STATUS']
    # For crying out loud with bloody tears, BOOK__ works for filter
    # but not for display >.> What gives...???

    def get_title(self, obj):
        return obj.BOOK.TITLE

    def get_author(self, obj):
        return obj.BOOK.AUTHOR

    def get_language(self, obj):
        return obj.BOOK.LANGUAGE


admin.site.register(BookCopy, BookCopyAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
