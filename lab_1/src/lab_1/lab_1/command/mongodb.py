import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient

# Підключення до MongoDB
client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
db = client['libraryy']

# Колекції
books_collection = db['books']
users_collection = db['users']

# Асинхронна функція для додавання книг
async def add_books():
    books = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Novel", "publishedYear": 1925, "available": True},
        {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "publishedYear": 1949, "available": True},
        {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Novel", "publishedYear": 1960, "available": False},
        {"id": 4, "title": "Moby-Dick", "author": "Herman Melville", "genre": "Adventure", "publishedYear": 1851, "available": True},
        {"id": 5, "title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical", "publishedYear": 1869, "available": False}
    ]
    result = await books_collection.insert_many(books)
    print(f"Added books with IDs: {result.inserted_ids}")

# Асинхронна функція для додавання користувачів
async def add_users():
    users = [
        {"name": "Alice", "age": 25, "email": "alice@example.com", "borrowedBookId": 3},
        {"name": "Bob", "age": 30, "email": "bob@example.com", "borrowedBookId": 1},
        {"name": "Charlie", "age": 22, "email": "charlie@example.com", "borrowedBookId": 2},
        {"name": "Diana", "age": 28, "email": "diana@example.com", "borrowedBookId": 5},
        {"name": "Eve", "age": 35, "email": "eve@example.com", "borrowedBookId": 4}
    ]
    result = await users_collection.insert_many(users)
    print(f"Added users with IDs: {result.inserted_ids}")

async def get_users_with_books():
    pipeline = [
        {
            "$lookup": {
                "from": "books",  # Колекція, з якою виконується об’єднання
                "localField": "borrowedBookId",  # Поле в колекції users
                "foreignField": "id",  # Поле в колекції books, з яким порівнюємо
                "as": "borrowedBook"  # Результат об'єднання додасться в це поле
            }
        },
        {
            "$unwind": "$borrowedBook"  # Розпакувати масив з однієї книги
        }
    ]

    async for user in users_collection.aggregate(pipeline):
        print(f"User: {user['name']}, Borrowed Book: {user['borrowedBook']['title']}")

async def get_all_books():
    books_cursor = books_collection.find({})
    books = await books_cursor.to_list(length=100)  # Отримати до 100 книг
    print("Books:")
    for book in books:
        print(book)

# Асинхронна функція для пошуку книги за автором
async def get_books_by_author(author_name):
    books_cursor = books_collection.find({"author": author_name})
    books = await books_cursor.to_list(length=100)
    print(f"Books by {author_name}:")
    for book in books:
        print(book)

# Асинхронна функція для отримання всіх користувачів
async def get_all_users():
    users_cursor = users_collection.find({})
    users = await users_cursor.to_list(length=100)  # Отримати до 100 користувачів
    print("Users:")
    for user in users:
        print(user)

# Асинхронна функція для пошуку користувача за іменем
async def get_user_by_name(user_name):
    user = await users_collection.find_one({"name": user_name})
    if user:
        print(f"User {user_name}: {user}")
    else:
        print(f"User {user_name} not found")

# Головна асинхронна функція для виконання додавання
async def add_values():
    await add_books()
    await add_users()

async def get_values():
    # Отримати всі книги
    await get_all_books()
    # Отримати всі книги певного автора
    await get_books_by_author("George Orwell")
    # Отримати всіх користувачів
    await get_all_users()
    # Отримати користувача за ім'ям
    await get_user_by_name("Alice")

def run_add_values():
    asyncio.run(add_values())

def run_get_values():
    asyncio.run(get_values())

def run_aggregated_values():
    asyncio.run(get_users_with_books())

# Run the asynchronous main function
if __name__ == "__main__":
   print("please run specific script")