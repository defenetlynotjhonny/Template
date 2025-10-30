from django.shortcuts import render

# Create your views here.

def homepage(request):
    """
    This view function is responsible for rendering the homepage.
    It just renders a simple HTML template.
    """
    # This will look for a template at 'core/templates/core/homepage.html'
    return render(request, 'homepage.html')


def about_page(request):
    """
    This view function is responsible for rendering the about page.
    It just renders a simple HTML template.
    """
    # This will look for a template at 'core/templates/core/about_page.html'
    return render(request, 'about_page.html')