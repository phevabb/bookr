from django.urls import path
from .views import *

urlpatterns = [

    path('create/', BookCreatView.as_view(), name='book_create'),
    path('update/<int:pk>', BookUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', BookDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>', BookDetailView.as_view(), name='detail')


]
