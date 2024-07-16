from django.contrib import auth
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=20, help_text="name of publisher")
    website = models.URLField(help_text="Publisher's website")
    email = models.EmailField(help_text="publisher's email")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=40)
    publication_date = models.DateField(verbose_name="date published")
    isbn = models.CharField(max_length=20)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField("Contributor", through="BookContributor")

    def __str__(self):
        return self.title


class Contributor(models.Model):
    first_names = models.CharField(max_length=50)
    last_names = models.CharField(max_length=50)
    email = models.EmailField(help_text="email of the contributor.")

    def __str__(self):
        return self.first_names


class ContributionRole(models.TextChoices):
    AUTHOR = "AUTHOR", "Author"
    CO_AUTHOR = "CO_AUTHOR", "Co-Author"
    EDITOR = "EDITOR", "Editor"


class BookContributor(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="Role of contributor.",
        choices=ContributionRole.choices,
        max_length=20,
    )


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the review was created."
    )
    date_edited = models.DateTimeField(
        null=True, help_text="The date and time the review was last edited."
    )
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="The Book that this review is for."
    )
