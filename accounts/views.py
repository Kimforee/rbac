from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import RegisterSerializer
from accounts.permissions import IsAdmin, IsModerator, IsAdminOrModerator
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from rest_framework.decorators import api_view, permission_classes
import logging

logger = logging.getLogger('django')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")  # Get the selected role from the form

        # Check if the passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("register")

        # Restrict the "admin" role to superusers only
        if role == "admin" and not request.user.is_superuser:
            messages.error(request, "You are not authorized to create an admin account.")
            return redirect("register")

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role  # Set the role based on the form input
        )

        # Assign superuser and staff status if the role is 'admin'
        if role == "admin":
            user.is_superuser = True
            user.is_staff = True

        user.save()  # Save to apply all changes

        # Assign the user to the corresponding group (Admin, Moderator, User)
        if role == "admin":
            admin_group = Group.objects.get(name="Admin")
            user.groups.add(admin_group)
        elif role == "moderator":
            moderator_group = Group.objects.get(name="Moderator")
            user.groups.add(moderator_group)
        else:
            user.groups.add(Group.objects.get(name="User"))

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

@login_required
def admin_view(request):
    if request.user.is_staff:  # Check if the user is an admin
        return render(request, "admin_view.html")
    messages.warning(request, "You are not authorized to access this page.")
    return redirect("home")
    

@login_required
def user_view(request):
    # Check if the user is neither Admin nor Moderator
    if not request.user.is_staff and hasattr(request.user, 'role') and request.user.role == "User":
        return render(request, "user_view.html")

    # Redirect Admins and Moderators
    messages.warning(request, "You are not authorized to access this page.")
    return redirect("home")

@login_required
def admin_moderator_view(request):
    # Check if user is an admin or moderator
    if request.user.is_staff or request.user.groups.filter(name='Moderator').exists():
        return render(request, "admin_moderator_view.html")
    messages.warning(request, "You are not authorized to access this page.")
    return redirect("home")

def drf(request):
    return render(request, "drf.html")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # Add the user's role to the response
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"User '{request.data.get('username')}' logged in successfully.")
            return response
        except InvalidToken:
            logger.warning(f"Failed login attempt for username: '{request.data.get('username')}'.")
            return Response({"error": "Invalid credentials"}, status=401)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        if not request.user.role == 'admin':
            logger.warning(f"Unauthorized access attempt by user '{request.user.username}' on AdminOnlyView.")
            return Response({"error": "Access denied."}, status=403)
        return Response({"message": "Hello Admin! You have access to this view."})

class ModeratorOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        return Response({"message": "Hello Moderator! You have access to this view."})

class AdminOrModeratorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrModerator]

    def get(self, request):
        return Response({"message": "Hello Admin/Moderator! You have access to this view."})

class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'user':
            return Response({"message": "Hello User! You have access to this view."})
        return Response({"message": "Access denied."}, status=403)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User '{request.user.username}' logged out successfully.")
            return Response({"message": "Logged out successfully."}, status=200)
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return Response({"error": "Something went wrong."}, status=400)

