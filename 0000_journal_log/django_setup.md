# Django Project Initialization and Structure Setup

## Step 1: Install Django
To start a new Django project, first, ensure that Django is installed:
```bash
pip install django
```

## Step 2: Create a New Django Project
Use the following command to create a new project:
```bash
django-admin startproject project_name
```
Replace `project_name` with the desired name of your project.

## Step 3: Project Structure
Once the project is created, it will have the following structure:
```
project_name/
├── manage.py          # Command-line utility for administrative tasks
├── project_name/      # Project package
│   ├── __init__.py    # Indicates that this directory should be treated as a Python package
│   ├── settings.py     # Configuration settings for the Django project
│   ├── urls.py         # URL declarations for the project
│   └── wsgi.py         # WSGI application callable for deploying the project
```

## Step 4: Run the Development Server
To verify that your project is set up correctly, navigate to the project directory and run:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your web browser to see your project in action.

## Conclusion
You have successfully initialized a Django project and set up its structure!