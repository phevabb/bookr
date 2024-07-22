from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
from .forms import MainSearch_form, PublisherForm, ReviewForm, BookForm, BookMediaForm
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from django.contrib import messages

# cbvs


def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save(False)
            cover = form.cleaned_data.get('cover')
            if cover:
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=image.format)
                book.cover.save(cover.name, image_data)
                book.save()
                messages.success(request, f'Book {book} was updated successfully')
                return redirect("detail_view", book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request, "reviews/instance_picture_form.html",
                  {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True})


def book_edit(request, bo_pk=None):
    if bo_pk is not None:
        book = get_object_or_404(Book, pk=bo_pk)
    else:
        book = None
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            updated_book = form.save()

            if book is None:
                messages.success(request, f" {updated_book.title} created successfully")
            else:
                messages.success(request, f"{book} updated successfully")
            return redirect("detail_view", updated_book.pk)

    else:
        form = BookForm(instance=book)
    return render(request, "reviews/editbook.html",
                  {"book_form": form, "instance": book, "model_type": "Book",
                   "book": book, })


def review_edit(request, b_pk=None, r_pk=None):
    #  First, create instance containers
    if b_pk is not None:
        book = get_object_or_404(Book, pk=b_pk)
    else:
        book = None

    if r_pk is not None:
        review = get_object_or_404(Review, pk=r_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, f"Review for {book}, created successfully")
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, f"Review for {book}, was updated successfully")
            updated_review.save()
            return redirect("detail_view", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance_review_form.html",
                  {"rev_form": form, "instance": review, "model_type": "Review",
                   "book": book, "related_model_type": Book})


#  this view can requests via the following:
#  1. a normal get from /publisher/new/
#  2. a post with or without key form "publisher/<int:pk>/
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)  # 1
        if form.is_valid():  # we must validate the data.
            updated_publisher = form.save()  # we save the data.
            if publisher is None:
                messages.success(request,
                                 f"Publisher '{updated_publisher}' was created successfully.")  # if no id was passed, we create a new publisher
            else:
                messages.success(request,
                                 f"Publisher '{updated_publisher}' was updated successfully.")  # if id was provided, we update the id.

            return redirect("publisher_edit", pk=updated_publisher.pk)  # 2
    else:
        form = PublisherForm(instance=publisher)

    return render(request, 'reviews/instance_form.html',
                  {"pub_form": form, 'instance': publisher, "model_type": "Publisher"})


# ?search=Emmanuel&title_contributor=Contributor&submit=submit
# purpose of this function is to pull all ratings on each book
def home(request):
    search_text = request.GET.get('search')
    # GET request passes through the url. anything that passes through the url is automatically a query dict
    mainform = MainSearch_form(request.GET)  # always create an instance of the form with the required method in it
    books = set()  # set is just used to prevent duplicates

    if mainform.is_valid() and mainform.cleaned_data['search']:
        search = mainform.cleaned_data['search']  # clean data means, already in list form. no need to use getlist
        search_in = mainform.cleaned_data.get('title_contributor')
        if search_in == 'Contributor':

            fname_contributors = Contributor.objects.filter(first_names__icontains=search)
            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            lname_contributors = Contributor.objects.filter(last_names__icontains=search)
            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)
        else:
            books = Book.objects.filter(
                title__icontains=search)  # It checks if the title field in Book model contains the string in search (it is case-insensitive).

    return render(request, 'reviews/home.html', {'mainform': mainform, "search_text": search_text, "books": books})


def detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            review_content = list(review.content for review in reviews)
            review_created_on = list(review.date_created for review in reviews)
            review_creator = list(review.creator for review in reviews)

            context = {
                "book": book,
                "book_rating": book_rating,
                "review_content": review_content,
                "review_created_on": review_created_on,
                "review_creator": review_creator,
                "reviews": reviews,
            }
        else:
            book_rating = None
            review_content = None
            review_created_on = None
            review_creator = None
            context = {
                "book": book,
                "book_rating": book_rating,
                "review_content": review_content,
                "review_created_on": review_created_on,
                "review_creator": review_creator,
                "reviews": None,
            }
        return render(request, "reviews/book_detail.html", context)


def books_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            review_content = list(review.content for review in reviews)

            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
            review_content = None
        book_list.append(
            {
                "book": book,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
                "review_content": review_content,
            }
        )
    contex = {"book_list": book_list}

    return render(request, "reviews/books_list.html", contex)

# title__icontains=search is a Django query lookup that performs a case-insensitive containment test.

########################### 1 ##############################
#  when we submit, an instance of formPublisher is created and its content, passed to form.
#  forms from forms.Model must have an instance.
#  it is just a container. if the request came in
#  with and pk, then the publisher with the associated id fills the container.
#  in this case we are only updating the publisher the id provided.

#  if the request came in with no pk, then it means the container is empty and we are creating a new container.


###################### 2 ###########################
#  note that when we passed in pk, (thus after submitting a form) the publisher in the database with that id is updated
#  also when we don't pass in pk, a new publisher is created. this new publisher has a newly created pk
#  this means, weather we pass in pk or not, in the end, there will be a pk


#  when we redirect to publisher_edit,
#  remember that publisher_edit needs
#  a pk( path("publisher/<int:pk>/", views.publisher_edit, name="publisher_edit"), )
#   that is why we do pk=updated_publisher.pk in (return redirect("publisher_edit", pk=updated_publisher.pk) )
#  just to pass the pk to publisher_edit
