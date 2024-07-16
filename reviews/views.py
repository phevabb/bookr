from django.shortcuts import get_object_or_404, render
from .forms import MainSearch_form
from .models import Book, Contributor
from .utils import average_rating

# ?search=Emmanuel&title_contributor=Contributor&submit=submit
# purpose of this function is to pull all ratings on each book
def home(request):
    search_text = request.GET.get('search', '')  # GET request passes through the url. anything that passes through the url is automatically a query dict
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
