# Test Project

This is a Django-based project that consists of three main apps: `hasnat_app`, `project_app`, and `bug_app`. The project manages user roles (developer, manager, QA), allows project creation, and tracks bugs.

## Apps Overview

### 1. `hasnat_app`
This app handles user management and authentication. The user roles include:
- **Developer**
- **Manager**
- **QA (Quality Assurance)**

#### Features:
- User registration (signup)
- User login
- User type selection (`join_us` to register as a specific user type: developer, manager, or QA)

#### Key Files:
- **models.py**: Defines a custom `User` model that extends Django’s `AbstractUser` with the `user_types` field.
- **views.py**: Contains views for user signup, login, and user type selection.
- **forms.py**: Defines the `UserForm` for user registration.

### 2. `project_app`
This app allows managers to create and list projects.

#### Features:
- **Project Creation**: Only users with the role of `Manager` can create projects.
- **Project List**: Displays a list of projects (also serves as the home page).

#### Key Files:
- **models.py**: Defines the `Project` model.
- **views.py**: Contains views for creating a project and listing all projects.

### 3. `bug_app`
This app handles bug tracking for each project. The app allows users to create and update bugs based on their roles.

#### Features:
- **Create Bug**: Managers and QA can create bugs for projects also can delete bugs.
- **Update Bug Status**: Developers can update the status of bugs (e.g., fixed, in progress).
- **Project Details**: View all bugs related to a project.

#### Key Files:
- **models.py**: Defines the `Bug` model.
- **views.py**: Contains views for creating bugs (`create_project_bug`) and viewing project details with all related bugs (`project_detail`).

## Installation

To set up this project locally, follow the steps below:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd test_project


python3 -m venv env
source env/bin/activate  , # On Windows, use `env\Scripts\activate`

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


Usage:
    User Signup: New users can register and select a user type (developer, manager, QA).
    Project Management: Managers can create and view projects.
    Bug Tracking: QA and Managers can create bugs for projects and also can delete bug, and developers can update the bug status.