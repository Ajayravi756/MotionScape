import os
import cv2
import tempfile
import moviepy.editor as mp
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from django.contrib.auth.models import User
from .utils import feature_extraction_external_video, predict
from .models import UploadedVideo  # Import UploadedVideo model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import customertbl , Admin  # Import the CustomerTbl model
from django.contrib.admin.views.decorators import staff_member_required
# from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def check_action(request):
    return render(request, 'checkaction.html')

def statistics(request):
    return render(request, 'statistics.html')

@login_required(login_url='index')
def LogoutPage(request):
    logout(request)
    return redirect('index')


def index_view(request):
    return render(request, 'index.html')

def about_login(request):
    # Logic for about_login view
    return render(request, 'about_login.html')  # Assuming you have an HTML template for about_login

def statistics_login(request):
    # Logic for statistics_login view
    return render(request, 'statistics_login.html')  # Assuming you have an HTML template for statistics_login



# Implement logic to check if the video is displaying properly
def is_video_displaying(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video is open and readable
    if not cap.isOpened():
        # Release the video capture object
        cap.release()
        return False
    
    # Release the video capture object
    cap.release()
    return True


def upload_video_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['video_file']
            video = UploadedVideo.objects.create(video_file=uploaded_file)
            video_path = video.video_file.path
            
            try:
                # Check if the uploaded video is displaying properly
                video_available = is_video_displaying(video_path)

                # Generate GIF
                gif_path = os.path.splitext(video_path)[0] + ".gif"
                clip = mp.VideoFileClip(video_path)
                clip.subclip(0, 5).resize(width=480).write_gif(gif_path)
                video.gif_file = gif_path
                
                # Generate image
                image_path = os.path.splitext(video_path)[0] + ".jpg"
                clip.save_frame(image_path, t=0)  # Save the first frame as image
                video.image_file = image_path
                video.save()

                # Process the uploaded video using the predict function
                external_video_features = feature_extraction_external_video(video_path)
                predicted_class_label = predict(external_video_features)

                # Pass the URL of the generated GIF file to the template
                return render(request, 'result.html', {'predicted_class_label': predicted_class_label, 'result_image': video.gif_file.url})
            except Exception as e:
                # Handle exceptions here
                print(e)
                pass
    else:
        form = VideoUploadForm()
    return render(request, 'checkaction.html', {'form': form})




def result_view(request, video_id):
    video = get_object_or_404(UploadedVideo, pk=video_id)
    video_path = video.video_file.path
    external_video_features = feature_extraction_external_video(video_path)
    predicted_class_label = predict(external_video_features)
    return render(request, 'result.html', {'video': video, 'predicted_class_label': predicted_class_label})

from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import customertbl

# registration tasks


def reg(request):
    if request.method == "POST":
        nam = request.POST.get("name")
        eml = request.POST.get("email")
        cnum = request.POST.get("contact_number")
        pword = request.POST.get("password")
        usernam = request.POST.get("uname")
        
        # Create a new user instance with pending approval
        new_user = customertbl.objects.create(nam=nam, eml=eml, cnum=cnum, password=pword, uname=usernam, is_pending_approval=True)
        
        # # Notify admin via email
        # notify_admin(new_user)
        
        # Redirect to a page indicating successful registration
        return HttpResponse("<h4>Successfully registered. Await admin approval.</h4> <a href='/registration'>Login </a>")
    return render(request, 'registration.html')

# def notify_admin(new_user):
#     admin_email = 'admin@example.com'  # Replace with admin's email address
#     subject = 'New User Registration Approval Required'
#     message = f'A new user ({new_user.nam}) has registered and requires approval.'
#     send_mail(subject, message, 'noreply@example.com', [admin_email])



# Approve and Reject User Registrations

@staff_member_required
def approve_user_registration(request, user_id):
    user = customertbl.objects.get(id=user_id)
    user.is_pending_approval = False  # Approve the user registration
    user.is_approved = True
    user.save()
    # Optionally, send an email notification to the user about their registration approval
    return redirect('admin_dashboard')

@staff_member_required
def reject_user_registration(request, user_id):
    user = customertbl.objects.get(id=user_id)
    user.delete()  # Reject and delete the user registration
    # Optionally, send an email notification to the user about their registration rejection
    return redirect('admin_dashboard')


# New views for managing pending registrations
@staff_member_required
def pending_registrations(request):
    # Get all users pending approval
    pending_users = customertbl.objects.filter(is_pending_approval=True)

    return render(request, 'pending_registrations.html', {'pending_users': pending_users})

@staff_member_required
def approve_user(request, user_id):
    user = customertbl.objects.get(id=user_id)
    user.is_pending_approval = False
    user.is_approved = True
    user.save()
    return redirect('pending_registrations')

@staff_member_required
def reject_user(request, user_id):
    user = customertbl.objects.get(id=user_id)
    user.delete()
    return redirect('pending_registrations')


@login_required(login_url='index')
def delete_user(request, user_id):
    user = get_object_or_404(customertbl, pk=user_id)
    user.delete()
    return redirect('admin_dashboard')  # Redirect to admin dashboard or relevant page after deletion



# Admin Dashboard View
@staff_member_required
def admin_dashboard(request):
    approved_users = customertbl.objects.filter(is_approved=True)
    pending_users = customertbl.objects.filter(is_pending_approval=True)
    print("Approved Users:", approved_users)  # Debug statement
    print("Pending Users:", pending_users)    # Debug statement
    return render(request, 'admin_dashboard.html', {'approved_users': approved_users, 'pending_users': pending_users})

# Login View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # Use Django's User model
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

# def login_view(request):
#     User = get_user_model()

#     if request.method == "POST":
#         username = request.POST.get('user')
#         password = request.POST.get('passw')

#         user = authenticate(username=username, password=password)




#         if user is not None:
#             if user.is_active:  # Check for active user
#                 login(request, user)
#                 if user.is_superuser:
#                     # Redirect to admin dashboard for superuser
#                     return redirect('admin_dashboard')
#                 else:
#                     # Redirect to user dashboard or relevant page
#                     return redirect('checkaction')
#             else:
#                 # Handle inactive user case
#                 return render(request, 'registration.html', {'msg': "Your account is inactive."})
#         else:
#             # Authentication failed, render login page with error message
#             return render(request, 'registration.html', {'msg': "Invalid username and password"})

#     # If request method is not POST, render login page
#     return render(request, 'checkaction.html')

# /////////////////////////////////////////////////////////////////////////////////


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import customertbl

def login_view(request):
    if request.method == "POST":
        user = request.POST.get('user')
        passw = request.POST.get('passw')
        
        # # Check if user is admin
        # admin_obj = Admin.objects.filter(username=user, password=passw).first()
        # if admin_obj:
        #     request.session['admin'] = admin_obj.id
        #     return redirect('admin_dashboard')  # Redirect to the admin dashboard
            
        # Check if user is regular user
        user_obj = customertbl.objects.filter(uname=user, password=passw).first()
        if user_obj:
            request.session['username'] = user
            request.session['password'] = passw
            request.session['idno'] = user_obj.id
            return redirect('checkaction')  # Redirect to the checkaction page
            
        # If user is neither admin nor regular user
        return render(request, 'registration.html', {'msg': "Invalid username and password"})

    return render(request, 'registration.html')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('passw')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'msg': 'Invalid username or password'})
    else:
        return render(request, 'admin_login.html')


def login_view(request):
    if request.method == "POST":
        user = request.POST.get('user')
        passw = request.POST.get('passw')
        user_obj = customertbl.objects.filter(uname=user, password=passw).first()
        if user_obj:
            request.session['username'] = user
            request.session['password'] = passw
            request.session['idno'] = user_obj.id
            return redirect('checkaction')  # Redirect to the checkaction page
        
         # If user is neither admin nor regular user
        return render(request, 'registration.html', {'msg': "Invalid username and password"})

    return render(request, 'registration.html')

# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from .models import customertbl

# def login_view(request):
#     if request.method == "POST":
#         user = request.POST.get('user')
#         passw = request.POST.get('passw')
        
#         # Check if user exists and password is correct
#         user_obj = customertbl.objects.filter(uname=user, password=passw).first()
#         if user_obj:
#             # Check if user is approved by admin
#             if user_obj.is_approved:
#                 # Set user details in session
#                 request.session['username'] = user
#                 request.session['password'] = passw
#                 request.session['idno'] = user_obj.id
                
#                 # Redirect to appropriate page
#                 return redirect('checkaction')  # Redirect to the checkaction page
#             else:
#                 return render(request, 'registration.html', {'msg': "Your account is pending approval by the admin."})
#         else:
#             return render(request, 'registration.html', {'msg': "Invalid username and password"})

#     return render(request, 'registration.html')
