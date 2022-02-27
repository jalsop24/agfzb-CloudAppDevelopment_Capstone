
from datetime import datetime
import logging
import json
from multiprocessing import context

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# from models import CarDealer, DealerReview
from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


API_URL = "https://265ca22c.eu-gb.apigw.appdomain.cloud/dealership-review"
DEALER_PATH = "/dealership"
REVIEWS_PATH = "/review"

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {
        "current": "About"
    }
    return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {
        "current": "Contact"
    }
    return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/register.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/register.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {
        "current": "Index"
    }
    if request.method == "GET":
        url = API_URL + DEALER_PATH
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = [
            {"id": dealer.id, "text": dealer.short_name} 
            for dealer in dealerships
            ]
        # Return a list of dealer short name
        context["dealers"] = dealer_names

        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = API_URL + REVIEWS_PATH
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        return render(request, "djangoapp/dealer_details.html", context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

