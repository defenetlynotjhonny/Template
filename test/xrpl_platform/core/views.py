from django.shortcuts import render

# Create your views here.

def homepage(request):
    """
    This view function is responsible for rendering the homepage.
    It just renders a simple HTML template.
    """
    # This will look for a template at 'core/templates/core/homepage.html'
    return render(request, 'core/homepage.html')