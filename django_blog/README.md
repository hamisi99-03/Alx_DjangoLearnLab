Overview

This Django authentication system provides user registration, login, logout, and profile management functionality. It combines Django’s built-in authentication views with custom forms and views to support an extended user profile, including optional fields such as profile picture and bio.

Features

User Registration (custom form extending UserCreationForm)

User Login & Logout (Django built-in authentication views)

Profile Management (editable email)

Secure password handling (Django hashing)

CSRF protection on all forms

Automatic profile creation using Django signals