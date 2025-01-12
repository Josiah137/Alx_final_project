# Library Management System API

## **Introduction**

The Library Management System API is designed to simplify the process of managing book loans and returns in a library. It enables users to borrow and return books, view available books, search by title or author, and access their borrowing history.

---

## **Features**

- Borrow books with availability checks.
- Return borrowed books and update status.
- View all available books.
- Search books by title or author.
- Access a logged-in user’s borrowing history.

---

## **Installation**

### **1. Clone the Repository**

```bash
$ git clone <repository_url>
$ cd library-management-system-api
```

### **2. Create a Virtual Environment**

```bash
$ python -m venv venv
$ source venv/bin/activate  # For Linux/Mac
$ venv\Scripts\activate   # For Windows
```

### **3. Install Dependencies**

```bash
$ pip install -r requirements.txt
```

### **4. Apply Migrations**

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### **5. Create a Superuser**

```bash
$ python manage.py createsuperuser
```

### **6. Run the Development Server**

```bash
$ python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## **API Endpoints**

### **Authentication**

- All endpoints require token-based authentication.
- Include the `Authorization` header in your requests:
  ```
  Authorization: Token <your_token>
  ```

### **1. Borrow a Book**

- **Endpoint:** `/api/books/borrow/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "book_id": 1
  }
  ```
- **Response:**
  - **Success:**
    ```json
    {
        "message": "You have successfully borrowed the book."
    }
    ```
  - **Error:**
    ```json
    {
        "error": "Sorry, No copies of the book are available for now."
    }
    ```

### **2. Return a Book**

- **Endpoint:** `/api/books/return/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "book_id": 1
  }
  ```
- **Response:**
  - **Success:**
    ```json
    {
        "message": "You have successfully returned the book."
    }
    ```
  - **Error:**
    ```json
    {
        "error": "You have not borrowed this book or have already returned it."
    }
    ```

### **3. View Borrowing History**

- **Endpoint:** `/api/books/history/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "book_title": "Introduction to Python",
          "author": "John Doe",
          "borrow_date": "2025-01-01T10:00:00Z",
          "return_date": "2025-01-10T15:00:00Z",
          "status": "RETURNED"
      },
      {
          "book_title": "Advanced Django",
          "author": "Jane Smith",
          "borrow_date": "2025-01-05T12:00:00Z",
          "return_date": null,
          "status": "BORROWED"
      }
  ]
  ```

### **4. Filter Available Books**

- **Endpoint:** `/api/books/available/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "Introduction to Python",
          "author": "John Doe",
          "number_of_copies_available": 3
      },
      {
          "id": 2,
          "title": "Learning REST APIs",
          "author": "Jane Doe",
          "number_of_copies_available": 1
      }
  ]
  ```

### **5. Search Books by Title or Author**

- **Endpoint:** `/api/books/search/`
- **Method:** `GET`
- **Query Parameter:** `?query=<search_term>`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "Advanced Django",
          "author": "Jane Smith",
          "number_of_copies_available": 2
      }
  ]
  ```

### **6. View All Books**

- **Endpoint:** `/api/books/`
- **Method:** `GET`
- **Response:**
  ```json
  [
      {
          "id": 1,
          "title": "Introduction to Python",
          "author": "John Doe",
          "number_of_copies_available": 3
      },
      {
          "id": 2,
          "title": "Advanced Django",
          "author": "Jane Smith",
          "number_of_copies_available": 0
      }
  ]
  ```

---

## **Database Models**

### **Book**

- `id`: Auto-incremented primary key.
- `title`: Title of the book.
- `author`: Author of the book.
- `number_of_copies_available`: Number of copies available for borrowing.

### **BookLog**

- `id`: Auto-incremented primary key.
- `user`: ForeignKey linking to the User model.
- `book`: ForeignKey linking to the Book model.
- `status`: Status of the transaction (`BORROWED` or `RETURNED`).
- `borrow_date`: Date and time the book was borrowed.
- `return_date`: Date and time the book was returned (nullable).

### **User**

- Managed by Django’s default User model.

---

## **Contributing**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

---
