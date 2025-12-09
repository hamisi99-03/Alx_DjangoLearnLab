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
