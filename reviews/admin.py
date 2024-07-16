from django.contrib import admin
from .models import Book, Publisher, Contributor, Review, BookContributor


##
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'rating', 'date_edited', 'creator', 'book')


class BookContributorAdmin(admin.ModelAdmin):
    list_display = ('book', 'contributor', 'role')


# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'isbn', 'title', )
    list_editable = ('title', )  # Make 'title', 'publisher', and 'isbn' editable
    list_display_links = ('publisher', 'isbn')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'email')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('first_names', 'last_names', 'email')


admin.site.register(Book, BookAdmin),
admin.site.register(Publisher, PublisherAdmin),
admin.site.register(Contributor, ContributorAdmin),
admin.site.register(Review, ReviewAdmin),
admin.site.register(BookContributor, BookContributorAdmin),
