# 👤 User and Profile Models — Safe Skill Academy

This module defines the **custom user model** and **profile system** used in the Safe Skill Academy project.  
It replaces Django’s default user model to use email-based authentication and automatically creates a user profile upon registration.

---

## 🧩 Overview

The system contains two main models:

1. **User** — A custom user model inheriting from Django’s `AbstractUser`.
2. **Profile** — An extension of the user model that stores additional user information.

---

## 🧱 Models

### 1. User Model

The `User` model customizes Django's default authentication to use **email** as the primary identifier.

#### Fields:
| Field | Type | Description |
|--------|------|-------------|
| `username` | CharField | Auto-generated from the email prefix if not provided |
| `email` | EmailField | Unique identifier for authentication |
| `full_name` | CharField | User's full name (auto-filled if empty) |
| `otp` | CharField | One-Time Password for verification (optional) |
| `refresh_token` | CharField | Optional field for session management or JWT refresh |

#### Customizations:
- **`USERNAME_FIELD = 'email'`** → Users log in using email instead of username.
- **Auto-filling:** If `full_name` or `username` is empty, it’s derived from the email prefix.
- **String Representation:** Returns the user's email.

#### Example:
```python
user = User.objects.create_user(
    email="example@gmail.com",
    password="mypassword123"
)
print(user.username)  # Output: example
print(user.full_name) # Output: example
