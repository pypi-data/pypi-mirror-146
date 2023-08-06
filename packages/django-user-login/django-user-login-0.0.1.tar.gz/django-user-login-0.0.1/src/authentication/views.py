from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from . import util
import random
from django.conf import settings

@ensure_csrf_cookie
def login_view(request):
    if request.session.get("register", False):
        request.session["register"].clear()
        request.session["register"] = None
    
    if request.session.get("recover", False):
        request.session["recover"].clear()
        request.session["recover"] = None
    
    if request.user.is_authenticated:
        return redirect('/')
    
    login_error = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            login_error = "Incomplete Form"
        else:
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
            if user and authenticate(request, username=user.username, password=password):
                login(request, user)
                q = dict(request.GET)
                if "next" in q:
                    return redirect(q["next"][0])
                return redirect('/')
            else:
                login_error = "Invalid Credentials"

    try:
        site_title = settings.SITE_TITLE
    except AttributeError:
        site_title = None
    
    context = {
        "sitetitle": site_title,
        "login_error":login_error
    }
    return render(
        request,
        'authentication/homepage.html',
        context
    )


def login_view_js(request):
    if request.method == "GET" or request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    username = request.POST["username"]
    password = request.POST["password"]

    user = User.objects.filter(Q(username=username) | Q(email=username)).first()
    if user and authenticate(request, username=user.username, password=password):
        login(request, user)
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "message": "Invalid Credentials"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))


def logout_view_js(request):
    logout(request)
    return JsonResponse({"success": True})


def register(request):
    if request.method == "GET" or request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    username = request.POST["username"]
    email = request.POST["email"]
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]

    if not first_name or not last_name or not username or not password2 or not email or not password1:
        return JsonResponse({"success": False, "message": "Incomplete Form"})
    
    username = username.strip().lower()
    if not util.validate_username(username):
        return JsonResponse({"success": False, "message": "Invalid Username"})
    
    if not util.validate_email(email):
        return JsonResponse({"success": False, "message": "Invalid Email Address"})
    
    if password1 != password2:
        return JsonResponse({"success": False, "message": "Passwords don't Match"})

    if not util.validate_password(password2):
        return JsonResponse({"success": False, "message": "Invalid Password"})
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"success": False, "message": "This username already exists."})
        
    if User.objects.filter(email=email).exists():
        return JsonResponse({"success": False, "message": "This email is associated with another account."})

    code = str(random.randint(100000, 999999))
    try:
        send_mail(
            'Verification Code',
            f'Your verification code is {code}.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except:
        return JsonResponse({"success": False, "message": "Something went wrong. Please try again later."})
    
    request.session["register"] = {
        "first_name": first_name.strip().lower().title(),
        "last_name": last_name.strip().lower().title(),
        "username": username,
        "email": email,
        "password": password1,
        "verified": False,
        "code": code
    }
    request.session.modified = True
    return JsonResponse({"success": True, "email": email})


def cancelRegistration(request):
    if request.session.get("register", False):
        request.session["register"].clear()
        request.session["register"] = None
    return JsonResponse({"success": True})


def resendVerificationCode(request):
    if request.user.is_authenticated or not request.session.get("register", False):
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    code = str(random.randint(100000, 999999))
    email = request.session["register"]["email"]
    try:
        send_mail(
            'Verification Code',
            f'Your verification code is {code}.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except:
        request.session["register"].clear()
        request.session["register"] = None
        return JsonResponse({"success": False, "message": "Something went wrong. Please try again later."})
    
    request.session["register"]["code"] = code
    request.session.modified = True
    return JsonResponse({"success": True})


def verifyRegistration(request):
    if request.user.is_authenticated or not request.session.get("register", False) or request.method == "GET":
        return JsonResponse({"success": False, "message": "Invalid Request"})

    code = request.POST["code"]
    if not code:
        return JsonResponse({"success": False, "message": "Incomplete Form"})
    if code != request.session["register"]["code"]:
        return JsonResponse({"success": False, "message": "Incorrect Code"})
    
    user = User.objects.create_user(
        request.session["register"]["username"],
        request.session["register"]["email"],
        request.session["register"]["password"]
    )
    
    user.first_name = request.session["register"]["first_name"]
    user.last_name = request.session["register"]["last_name"]
    user.save()

    request.session["register"].clear()
    request.session["register"] = None
    return JsonResponse({"success": True})


def recover(request):
    if request.user.is_authenticated or request.method == "GET":
        return JsonResponse({"success": False, "message": "Invalid Request"})

    username = request.POST["username"]
    if not username:
        return JsonResponse({"success": False, "message": "Incomplete Form"})
    
    user = User.objects.filter(Q(username=username) | Q(email=username)).first()
    if not user:
        return JsonResponse({"success": False, "message": "Invalid Credentials"})
    
    code = str(random.randint(100000, 999999))
    email = user.email
    try:
        send_mail(
            'Verification Code',
            f'Your verification code is {code}.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except:
        return JsonResponse({"success": False, "message": "Something went wrong. Please try again later."})
    
    request.session["recover"] = {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "verified": False,
        "code": code
    }
    request.session.modified = True
    return JsonResponse({"success": True, "email": util.encryptemail(user.email)})


def cancelRecovery(request):
    if request.session.get("recover", False):
        request.session["recover"].clear()
        request.session["recover"] = None
    return JsonResponse({"success": True})


def resendRecoveryCode(request):
    if request.user.is_authenticated or not request.session.get("recover", False):
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    code = str(random.randint(100000, 999999))
    email = request.session["recover"]["email"]
    try:
        send_mail(
            'Verification Code',
            f'Your verification code is {code}.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except:
        request.session["recover"].clear()
        request.session["recover"] = None
        return JsonResponse({"success": False, "message": "Something went wrong. Please try again later."})
    
    request.session["recover"]["code"] = code
    request.session["recover"]["verified"] = False
    request.session.modified = True
    return JsonResponse({"success": True})


def verifyRecovery(request):
    if request.user.is_authenticated or not request.session.get("recover", False) or request.method == "GET":
        return JsonResponse({"success": False, "message": "Invalid Request"})
    code = request.POST["code"]
    if not code:
        return JsonResponse({"success": False, "message": "Incomplete Form"})
    if code != request.session["recover"]["code"]:
        return JsonResponse({"success": False, "message": "Incorrect Code"})
    
    request.session["recover"]["verified"] = True
    request.session.modified = True
    return JsonResponse({"success": True, "username": request.session["recover"]["username"]})


def changepassword(request):
    if request.user.is_authenticated or not request.session.get("recover", False) or not request.session["recover"]["verified"] or request.method == "GET":
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    password1 = request.POST["password1"]
    password2 = request.POST["password2"]

    if not password1 or not password2:
        return JsonResponse({"success": False, "message": "Incomplete Form"})
    
    if password2 != password1:
        return JsonResponse({"success": False, "message": "Passwords Don't Match"})
    
    if not util.validate_password(password1):
        return JsonResponse({"success": False, "message": "Invalid Password"})

    try:
        user = User.objects.get(id=request.session["recover"]["user_id"])
    except:
        return JsonResponse({"success": False, "message": "Invalid Request"})
    
    user.set_password(password1)
    user.save()
    request.session["recover"].clear()
    request.session["recover"] = None
    email = user.email
    try:
        send_mail(
            'Security Information',
            'Your password was just changed.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )
    except:
        pass
    return JsonResponse({"success": True})