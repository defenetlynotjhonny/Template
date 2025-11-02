from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
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

def payment_page(request):
    """
    This view function is responsible for rendering the payment page.
    It just renders a simple HTML template.
    """
    # This will look for a template at 'core/templates/core/payment_page.html'
    return render(request, 'payment_page.html')


def api_data(request):
    """
    A simple API endpoint that returns a fixed set of data as JSON.
    """
    # This is the data that will be sent as JSON
    data = {
        'name': 'My API',
        'version': '1.0',
        'data': [1, 2, 3, 4]
    }
    
    # JsonResponse serializes the dictionary into a JSON string
    # and returns it with the correct 'application/json' content type.
    return JsonResponse(data)




def login_page_view(request):
    """
    Serves the crypto key login.html page.
    """
    return render(request, 'login.html')

@csrf_exempt  # Disables CSRF token check for this view
def api_post_data(request):
    """
    API endpoint that accepts POST requests with JSON data.
    """
    # Only allow POST requests
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data from the request body
            data = json.loads(request.body)
            
            # You can now work with the data
            # For this example, we'll just echo it back with a message.
            received_name = data.get('name', 'Guest')
            
            response_data = {
                'status': 'success',
                'message': f"Hello, {received_name}! Your data was received.",
                'data_received': data
            }
            return JsonResponse(response_data, status=200)
            
        except json.JSONDecodeError:
            # Handle cases where the request body is not valid JSON
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
    elif request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': 'GET method not allowed for this endpoint'}, status=405)
    
    # Handle other methods (like GET) with an error
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)



@csrf_exempt # Disable CSRF for this JSON endpoint
def api_key_login(request):
    """
    Handles the incoming secret key from the login page.
    It does NOT perform login; it just prints the key and returns success.
    
    *** SECURITY WARNING: Never print or log secret keys in production! ***
    """
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Only POST method is allowed"}, 
            status=405
        )

    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        secret_key = data.get("secret_key")

        if not secret_key:
            return JsonResponse(
                {"status": "error", "message": "No 'secret_key' provided"}, 
                status=400
            )

        # --- THIS IS THE KEY PART ---
        # Instead of logging in, we just print the data to the server console.
        # This is purely for demonstration.
        print("--- SECRET KEY RECEIVED (DEMO) ---")
        print(f"Received key: {secret_key}")
        print("------------------------------------")
        
        # You could also print the whole dictionary
        # print(f"Received data: {data}")

        # Send a success response back to the JavaScript
        return JsonResponse(
            {"status": "success", "message": "Key received and printed to console."},
            status=200
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"status": "error", "message": "Invalid JSON format"}, 
            status=400
        )
    except Exception as e:
        # Catch other potential errors
        print(f"An error occurred: {e}")
        return JsonResponse(
            {"status": "error", "message": "An internal server error occurred"}, 
            status=500
        )
