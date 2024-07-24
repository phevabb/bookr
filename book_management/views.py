from django.shortcuts import render

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views import View
from .forms import BookForm
from .models import Book


#  form template combiner
class BookRecordFormView(FormView):
    template_name = 'book_management/book_form.html'
    form_class = BookForm


#  create c
class BookCreatView(CreateView):
    model = Book
    fields = ['name', 'author']
    template_name = 'book_management/book_form.html'
    success_url = '/'

#  read R
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_management/book_detail.html'


#  update
class BookUpdateView(UpdateView):
    model = Book
    fields = ['name', 'author']
    template_name = 'book_management/book_form.html'
    success_url = '/'


#  Delete
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_management/book_delete_form.html'
    success_url = '/'

    def get_queryset(self):
        # This is optional, only if you need custom queryset logic
        return Book.objects.all()



