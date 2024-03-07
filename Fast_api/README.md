# FastAPI Book Review System
Assessment - RESTful API using FastAPI for a hypothetical book review system.

This project implements a simple book review system using FastAPI, SQLAlchemy for database operations, and Pydantic for data validation. It allows users to perform CRUD operations on books and reviews, as well as sending confirmation emails for reviews.

1. Installation
    Clone the repository:

    git clone https://github.com/your_username/fastapi-book-review-system.git

2. Install dependencies:

    pip install -r requirements.txt

3. Run the FastAPI server:

    uvicorn main:app --reload

4. Usage & Endpoints

    POST /books/: Create a new book.
    GET /books/{book_id}/: Get a specific book by ID.
    PUT /books/{book_id}/: Update a book's details.
    DELETE /books/{book_id}/: Delete a book.
    GET /books/: Get a list of books, optionally filtered by author or publication year.
    GET /books/{book_id}/reviews/: Get a list of reviews for a book.
    POST /books/{book_id}/reviews/: Add a review for a book.
    PUT /books/{book_id}/reviews/{review_id}/: Update a review's details.
    DELETE /books/{book_id}/reviews/{review_id}/: Delete a review.
    POST /books/{book_id}/reviews/{review_id}/confirm/: Confirm a review and send a confirmation email.

# Models
BookCreate: Pydantic model for creating a book.
ReviewCreate: Pydantic model for creating a review.
BookResponse: Pydantic model for returning book data.
ReviewResponse: Pydantic model for returning review data.

# Database
This project uses SQLite as the database. The database file (test.db) will be created in the project directory.
To run DB file, 
    python test.py


# Testing
To run tests, use the following command:

    pytest test_main_app.py


#####################################################################################################################################
## Here are all the endpoints for Postman with examples:

# Add a Book
Endpoint: POST /books/
Body (JSON):

    {
    "title": "Example Book",
    "author": "John Doe",
    "publication_year": 2022
    }

Example Response:
json

    {
    "id": 1,
    "title": "Example Book",
    "author": "John Doe",
    "publication_year": 2022
    }


# Get a Book
Endpoint: GET /books/{book_id}/
Example: GET /books/1/
Update a Book

Endpoint: PUT /books/{book_id}/
Body (JSON):
json

    {
    "title": "Updated Book Title"
    }
Example: PUT /books/1/

# Delete a Book
Endpoint: DELETE /books/{book_id}/
Example: DELETE /books/1/

# Get Books
Endpoint: GET /books/
Example: GET /books/?author=sonu

# Get Reviews for a Book
Endpoint: GET /books/{book_id}/reviews/
Example: GET /books/1/reviews/

# Add a Review for a Book
Endpoint: POST /books/{book_id}/reviews/
Body (JSON):
json

    {
    "text": "Great book!",
    "rating": 5
    }
Example: POST /books/1/reviews/

# Update a Review
Endpoint: PUT /books/{book_id}/reviews/{review_id}/
Body (JSON):
json

    {
    "rating": 4
    }
Example: PUT /books/1/reviews/1/

# Delete a ReviewW
Endpoint: DELETE /books/{book_id}/reviews/{review_id}/
Example: DELETE /books/1/reviews/1/

# Confirm a Review and Send Email
Endpoint: POST /books/{book_id}/reviews/{review_id}/confirm/
Example: POST /books/1/reviews/1/confirm/

# To get all books published in a specific year:
Endpoint: GET /books/{publication_year}/
Example: GET http://localhost:8001/books/?publication_year=2022

# To get all books by a specific author:
Endpoint: GET http://localhost:8001/books/?author={}
Example: GET http://localhost:8001/books/?author=sonu

# To get all books by a specific author published in a specific year:
Endpoint: GET /books/{author}&{publication_year}
Example: GET http://localhost:8001/books/?author=SK&publication_year=2022


These are the endpoints you can use in Postman to interact with your FastAPI application. Adjust the {book_id} and {review_id} placeholders in the URLs as needed.


#####################################################################################################################################
# To run the test file test_main_app.py, you can use a test runner like pytest. 
First, make sure you have pytest installed. If not, you can install it using pip:

    pip install pytest

Then, you can run the tests by executing the following command in your terminal in the same directory as your test_main_app.py file:
    pytest test_main_app.py

This command will search for and run any test functions in the test_main_app.py file and display the test results in the terminal.
#####################################################################################################################################
