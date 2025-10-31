
## Run the project

cd ./xrpl_platform
python manage.py runserver

------------------------------------------------------------------------------------------------------------------------------

1. The Project Root (xrpl_platform/ outer folder)

This is the main container for your project. The files here manage the entire project.

manage.py This is your project's command-line utility. It's how you interact with your project. You use it to run commands like:

python manage.py runserver (starts the development server)

python manage.py startapp <name> (creates a new app)

python manage.py migrate (updates your database)

db.sqlite3 This is your database file. Django created it when you ran the migrate command. For development, Django uses this simple file to store all your data (like users, blog posts, etc.).

2. The Project Configuration Folder (xrpl_platform/xrpl_platform/ inner folder)

This folder is the central "brain" or configuration for your entire project. Its name is the same as the project root.

settings.py This is the most important file here. It holds all your project's settings:

INSTALLED_APPS: The list of all apps in your project (this is where you registered core).

DATABASES: Configuration for your database (like the db.sqlite3 file).

STATIC_URL: How to handle static files (CSS, JS).

SECRET_KEY: A unique key for your project's security.

urls.py This is the main URL router for your entire website. It's the "table of contents." When a user visits a URL, this file is the first place Django looks. It directs the request to the correct app (like you did by adding path('', include('core.urls'))).

wsgi.py / asgi.py These are server entry points. They are files that a production (live) web server uses to connect to and run your Django application. You don't need to edit them for now.

WSGI (Web Server Gateway Interface) is the standard for most Django projects.

ASGI (Asynchronous Server Gateway Interface) is newer and used for features that need real-time connections (like chat apps).

3. The App Folder (core/)

This is a Django "app." An app is a self-contained module that handles one specific feature of your website (like a blog, a user profile system, or, in your case, the "core" pages like the homepage).

views.py This is where your logic goes. Each function (or class) in this file corresponds to a different page. For example, your homepage function gets a request from the user and renders the homepage.html template.

models.py This is where you define your database schema. You create classes in this file, and each class represents a table in your database. For example, you might create a class Post(models.Model): to store blog posts.

urls.py This is the URL router for the core app only. It lists all the URLs that the core app is responsible for (like your homepage path ''). This file is "included" by the main urls.py in the project configuration folder.

templates/ You created this folder. It correctly holds the HTML files (templates) that your views.py will render.

static/ You also created this folder. It holds the static assets for this app only (like CSS, JS, or images specific to your core app).

migrations/ This folder stores the history of your database models. When you change models.py and run python manage.py makemigrations, Django creates a new "instruction" file in this folder. When you run migrate, Django reads these files to update your database.

admin.py This file is for registering your models with Django's built-in admin panel. If you create a Post model, you'd add a line here to make it show up on the /admin page so you can easily create, edit, and delete posts.

apps.py This is a small configuration file for the app itself. You used it when you added 'core.apps.CoreConfig' to your INSTALLED_APPS list in settings.py.

tests.py This is where you write automated tests to make sure your views.py and models.py code works as expected.

Other Files (Environment & Context)

These aren't Django files, but they are essential to your project.

.venv/: Your virtual environment. It's a private folder that holds all the Python packages (like Django) for this project only.

.gitignore: Tells Git (version control) which files to ignore (like .venv, __pycache__, and db.sqlite3).

requirements.txt: A list of all Python packages your project needs. This allows another developer to set up the project by just running pip install -r requirements.txt.

__pycache__/: Python automatically creates these folders to store compiled "bytecode" to make your app start faster. You can safely ignore them.

test.py: The file you created to test if Python was installed. It's not used by Django.


------------------------------------------------------------------------------------------------------------------------------
Here is that checklist. Let's use an "About Us" page as the example.

1. Create the HTML file:

Folder: core/templates/core/

Action: Create a new file named about.html in this folder.

Content: Add your HTML skeleton, just like you did for homepage.html.

2. Create the View function:

File: core/views.py

Action: Add a new Python function to this file.

Code:

Python
def about_page(request):
    return render(request, 'core/templates/core/about.html')
3. Register the URL:

File: core/urls.py

Action: Add a new path to your urlpatterns list.

Code:

Python
urlpatterns = [
    path('', views.homepage, name='homepage'),
    # Add this new line:
    path('about/', views.about_page, name='about'),
]
That's it. After those three steps, you can run the server and your new page will be live at http://127.0.0.1:8000/about/.