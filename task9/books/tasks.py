from celery import shared_task

from .models import Book, Notification
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Book, Review, Notification


@shared_task
def create_book():
    print("creating book")
    Book.objects.create(
        title="book",
        author="author",
        image='',
        genre="genre",
        price=100,
        desc="desc",
    )
    return "book created successfully"



@shared_task
def create_notification():
    print("Creating Notification")

    # Find the highest rated book
    highest_rated_book = Book.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating').first()

    if highest_rated_book:
        message = f"The highest rated book is {highest_rated_book.title} with an average rating of {highest_rated_book.avg_rating}"
        book_url = f"/books/{highest_rated_book.id}" 

        for user in User.objects.all():
            Notification.objects.create(
                user=user,
                message=message,
                book_url=book_url,
            )

        return "Notification created successfully"
    else:
        return "No books found"