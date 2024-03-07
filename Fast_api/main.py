from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import List, Optional
from mailer import send_email

# Create FastAPI app
app = FastAPI()

# SQLite database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define database models
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)

    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")


Base.metadata.create_all(bind=engine)

# Pydantic models for data validation
class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int = Field(..., ge=0)


class ReviewCreate(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int

    class Config:
        orm_mode = True


class ReviewResponse(BaseModel):
    id: int
    book_id: int
    text: str
    rating: int

    class Config:
        orm_mode = True


# CRUD operations for books
def get_book(book_id: int):
    with SessionLocal() as session:
        return session.query(Book).filter(Book.id == book_id).first()

def create_book(book: BookCreate):
    with SessionLocal() as session:
        db_book = Book(**book.dict())
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        return db_book

def update_book(book_id: int, book_data: BookCreate):
    with SessionLocal() as session:
        db_book = session.query(Book).filter(Book.id == book_id).first()
        if db_book:
            for key, value in book_data.dict(exclude_unset=True).items():
                setattr(db_book, key, value)
            session.commit()
            session.refresh(db_book)
        return db_book

def delete_book(book_id: int):
    with SessionLocal() as session:
        db_book = session.query(Book).filter(Book.id == book_id).first()
        if db_book:
            session.delete(db_book)
            session.commit()
        return db_book

def get_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    with SessionLocal() as session:
        query = session.query(Book)
        if author:
            query = query.filter(Book.author == author)
        if publication_year:
            query = query.filter(Book.publication_year == publication_year)
        return query.all()

# CRUD operations for reviews
def get_reviews(book_id: int):
    with SessionLocal() as session:
        return session.query(Review).filter(Review.book_id == book_id).all()

def create_review(book_id: int, review: ReviewCreate):
    with SessionLocal() as session:
        db_review = Review(**review.dict(), book_id=book_id)
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        return db_review

def update_review(review_id: int, review_data: ReviewCreate):
    with SessionLocal() as session:
        db_review = session.query(Review).filter(Review.id == review_id).first()
        if db_review:
            for key, value in review_data.dict(exclude_unset=True).items():
                setattr(db_review, key, value)
            session.commit()
            session.refresh(db_review)
        return db_review

def delete_review(review_id: int):
    with SessionLocal() as session:
        db_review = session.query(Review).filter(Review.id == review_id).first()
        if db_review:
            session.delete(db_review)
            session.commit()
        return db_review

# Define API endpoints

@app.post("/books/", response_model=BookResponse)
def add_book(book: BookCreate):
    return create_book(book)

@app.get("/books/{book_id}/", response_model=BookResponse)
def read_book(book_id: int):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}/", response_model=BookResponse)
def update_book_details(book_id: int, book: BookCreate):
    updated_book = update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}/", response_model=BookResponse)
def remove_book(book_id: int):
    deleted_book = delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

@app.get("/books/", response_model=List[BookResponse])
def read_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    return get_books(author, publication_year)

@app.get("/books/{book_id}/reviews/", response_model=List[ReviewResponse])
def get_book_reviews(book_id: int):
    return get_reviews(book_id)

@app.post("/books/{book_id}/reviews/", response_model=ReviewResponse)
def add_review(book_id: int, review: ReviewCreate):
    return create_review(book_id, review)

@app.put("/books/{book_id}/reviews/{review_id}/", response_model=ReviewResponse)
def update_review_details(book_id: int, review_id: int, review: ReviewCreate):
    updated_review = update_review(review_id, review)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@app.delete("/books/{book_id}/reviews/{review_id}/", response_model=ReviewResponse)
def remove_review(review_id: int):
    deleted_review = delete_review(review_id)
    if not deleted_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return deleted_review

@app.post("/books/{book_id}/reviews/{review_id}/confirm/", response_model=None)
def confirm_review(book_id: int, review_id: int, background_tasks: BackgroundTasks):
    with SessionLocal() as session:
        review = session.query(Review).filter_by(id=review_id, book_id=book_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        # Send email confirmation
        background_tasks.add_task(
            send_email, "Subject", "Hello, this is a test email.", "sonumandal048@gmail.com"
        )
        return {"message": "Confirmation email will be sent"}

# main fun 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
