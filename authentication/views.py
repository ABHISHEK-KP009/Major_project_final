
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from gfg import settings
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import password_validation
import re
# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
            #return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords doesn't match")
            #return redirect('home')
        
        alphanumeric = re.compile(r'^[0-9a-zA-Z]+$')
        if not alphanumeric.match(username):
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')
        # Create a new user instance user is created here
        try:
            validate_password(pass1)
        except DjangoValidationError as validation_error:
            messages.error(request, validation_error.messages[0])
            return redirect('home')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        
        # Set the additional fields
        myuser.first_name = fname
        myuser.last_name = lname
        
        # Save the user instance
        myuser.save()
        
        # Assign a unique user ID
        #myuser.is_active = False
        myuser.user_id = myuser.id

        myuser.save()
        
        messages.success(request, "Your Account has been successfully created.")

        # Welcome Email
        # subject = "Welcome to Online Examination System!!"
        # message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Online Examination System!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking you \n Nandan"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email

        return redirect('signin')
    
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname=user.first_name
            return redirect('../question1')
            # return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')
    return render(request, "authentication/signin.html")

def question1(request):
    if request.method == 'POST':
        return redirect('../question2')
    return render(request, 'authentication/question1.html')

def question2(request):
    if request.method == 'POST':
        pass
    return render(request, 'authentication/question2.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succcessfully!")
    return redirect('home')
