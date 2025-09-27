from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Request -> Response
# Request handler
# Action 

# View is usually for rendering HTML pages, for someone to see but in Django that's a template

def calculate():
    x = 1
    y = 2
    return x

def say_hello(request):
    # Pull data from the database (models)
    # return HttpResponse("Hello World from the blog index view!")
    x = calculate()
    return render(request, "hello.html", {"name": "Django"})