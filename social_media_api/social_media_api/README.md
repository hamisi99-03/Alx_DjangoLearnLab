Django Social Media API Authentication

Project Setup

Requirements

Python 3.x

Django

Django REST Framework

Django REST Framework Authtoken

Installation

pip install django djangorestframework
pip install djangorestframework-authtoken

Configuration

Add to INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]

Set custom user model:

AUTH_USER_MODEL = 'accounts.CustomUser'

Run migrations:

python manage.py makemigrations
python manage.py migrate

 User Model

Custom user model extends AbstractUser with:

bio (TextField)

profile_picture (ImageField)

followers (ManyToManyField to self, symmetrical=False)

 Authentication System

Serializers

RegistrationSerializer: Handles user signup, hashes password, saves bio and profile picture.

LoginSerializer: Validates username/password, returns authenticated user.

Views

RegisterView (CreateAPIView): Creates new users.

LoginView (APIView): Authenticates credentials, returns token.

TokenView (APIView): Retrieves token for authenticated user.

URL Patterns (accounts/urls.py)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', TokenView.as_view(), name='profile'),
]

Include in project-level urls.py:

path('api/accounts/', include('accounts.urls')),

 Testing

Start server

python manage.py runserver

Register User

Endpoint: POST /api/accounts/register/

Body:

{
  "username": "hamisi",
  "email": "hamisi@example.com",
  "password": "pass123",
  "bio": "Backend developer"
}

Login User

Endpoint: POST /api/accounts/login/

Body:

{
  "username": "hamisi",
  "password": "pass123"
}

Response:

{
  "token": "abc123xyz..."
}

Authenticated Requests

Include header:

Authorization: Token abc123xyz...

 Deliverables

Project Setup Files: settings.py, urls.py, migrations.

Code Files: models.py, serializers.py, views.py, urls.py in accounts app.

Documentation: This README with setup instructions, usage examples, and overview of the user model.

Notes

Extend TokenView to return user profile details.

Use Postman or curl for API testing.

Ensure media files are served correctly for profile_picture uploads.


testing results 
Postman test
login 
{
    "token": "2950b03c56e4019f4122b92a95665750f0e186f9"
}
create post 
{
    "id": 2,
    "title": "post by job",
    "content": "mehn i relly want an s1k",
    "author": "job",
    "created_at": "2025-12-10T13:37:28.959741Z",
    "updated_at": "2025-12-10T13:37:28.959741Z"
}

lists posts
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "title": "post by job",
            "content": "mehn i relly want an s1k",
            "author": "job",
            "created_at": "2025-12-10T13:37:28.959741Z",
            "updated_at": "2025-12-10T13:37:28.959741Z"
        },
        {
            "id": 1,
            "title": "My First Post",
            "content": "Hello world!",
            "author": "hamisi",
            "created_at": "2025-12-10T13:23:58.675816Z",
            "updated_at": "2025-12-10T13:23:58.675816Z"
        }
    ]
}

search posts Get/api/posts/?search=Hello
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "My First Post",
            "content": "Hello world!",
            "author": "hamisi",
            "created_at": "2025-12-10T13:23:58.675816Z",
            "updated_at": "2025-12-10T13:23:58.675816Z"
        }
    ]
}
create comment 
{
    "id": 2,
    "post": 2,
    "author": "job",
    "content": "dreams",
    "created_at": "2025-12-10T13:45:29.256942Z",
    "updated_at": "2025-12-10T13:45:29.256942Z"
}

Posts & Comments API Documentation
🔑 Authentication
- Method: Token Authentication
- Header format:
Authorization: Token <your_token>
Content-Type: application/json
- Obtain token via /api/token-auth/ (or your accounts login endpoint).
- Without this header, protected endpoints will return:
{ "detail": "Authentication credentials were not provided." }



📌 Posts Endpoints
1. List Posts
- Endpoint: GET /api/posts/
- Description: Retrieve all posts, paginated.
- Query Parameters:
- search → filter by title/content
- page → page number
- page_size → number of results per page
- Response Example:
lists posts
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "title": "post by job",
            "content": "mehn i relly want an s1k",
            "author": "job",
            "created_at": "2025-12-10T13:37:28.959741Z",
            "updated_at": "2025-12-10T13:37:28.959741Z"
        },
        {
            "id": 1,
            "title": "My First Post",
            "content": "Hello world!",
            "author": "hamisi",
            "created_at": "2025-12-10T13:23:58.675816Z",
            "updated_at": "2025-12-10T13:23:58.675816Z"
        }
    ]
}



2. Create Post
- Endpoint: POST /api/posts/
- Permissions: Authenticated users only.
- Request Body:
{
  "title": "Post by job",
  "content": "mehn i really want an s1k."
}
- Response Example:
create post 
{
    "id": 2,
    "title": "post by job",
    "content": "mehn i relly want an s1k",
    "author": "job",
    "created_at": "2025-12-10T13:37:28.959741Z",
    "updated_at": "2025-12-10T13:37:28.959741Z"
}



3. Retrieve Post
- Endpoint: GET /api/posts/{id}/
- Description: Get details of a single post.

4. Update Post
- Endpoint: PATCH /api/posts/{id}/
- Permissions: Only the author can update.
- Request Body:
{
  "title": "Updated Title"
}



5. Delete Post
- Endpoint: DELETE /api/posts/{id}/
- Permissions: Only the author can delete.

💬 Comments Endpoints
1. List Comments
- Endpoint: GET /api/comments/
- Description: Retrieve all comments, paginated.
- Response Example:
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "post": 1,
      "author": "hamisi",
      "content": "Nice post!",
      "created_at": "2025-12-10T14:10:00Z",
      "updated_at": "2025-12-10T14:10:00Z"
    }
  ]
}



2. Create Comment
- Endpoint: POST /api/comments/
- Permissions: Authenticated users only.
- Request Body:
{
  "post": 2,
  "content": "dreams"
}
- Response Example:
create comment 
{
    "id": 2,
    "post": 2,
    "author": "job",
    "content": "dreams",
    "created_at": "2025-12-10T13:45:29.256942Z",
    "updated_at": "2025-12-10T13:45:29.256942Z"
}



3. Retrieve Comment
- Endpoint: GET /api/comments/{id}/
- Description: Get details of a single comment.

4. Update Comment
- Endpoint: PATCH /api/comments/{id}/
- Permissions: Only the author can update.
- Request Body:
{
  "content": "Edited comment"
}



5. Delete Comment
- Endpoint: DELETE /api/comments/{id}/
- Permissions: Only the author can delete.

⚙️ Pagination & Filtering
- Pagination: ?page=2&page_size=5
- Filtering (Posts only): ?search=keyword


