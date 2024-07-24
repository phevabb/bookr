from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from reviews .views import profile
from django.urls import path, include

urlpatterns = [
    path('bm/', include('book_management.urls')),
    path("admin/", admin.site.urls),
    path('', include('reviews.urls')),
    path("accounts/profile/", profile, name='profile')
] + debug_toolbar_urls()
