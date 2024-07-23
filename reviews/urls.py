from django.urls import path
from django.conf import settings
from . import views, views2
from django.conf.urls.static import static

urlpatterns = [
    path("books/", views.books_list, name="books_list"),
    path("book/<int:pk>/", views.detail_view, name="detail_view"),
    path("", views.home, name="home"),
    #  for edit publisher
    path("publisher/<int:pk>/", views.publisher_edit, name="publisher_edit"),
    path('publisher/new/', views.publisher_edit, name='publisher_create'),

    #  edit book
    path("book/new/", views.book_edit, name='create_book'),
    path('book/edit/<int:bo_pk>/', views.book_edit, name='edit_book'),

    # for editing review
    path("review/<int:b_pk>/<int:r_pk>/", views.review_edit, name="review_edit"),
    path('review/new/<int:b_pk>/', views.review_edit, name='review_create'),

    #  for media
    path("books/media/<int:pk>", views.book_media, name='book_media'),



    #  Auths

    path("login/", views2.LoginView.as_view(), name="login"),
    path("accounts/login/", views2.LoginView.as_view(), name="login"),
    path("logout/", views2.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views2.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views2.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views2.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views2.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views2.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views2.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
