from django.shortcuts import render
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from functools import reduce
from django.db.models import Sum
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from django.http import Http404

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from .models import (
    Support,
    Notification
)

User = get_user_model()

from .constants import (
    CITIZENSHIP_STATUSES,
    MARITAL_CHOICES,
    PREFERRED_CURRENCY,
    PROGRAM_TYPES,
)


# Create your views here.


# -------------------------------- WEBSITE PAGES-------------------------------------
def home_page(request):
    return render(request, "website/index.html", {} )



# -------------------------------- AUTH PAGES----------------------------------------
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    return render(request, "dashboard/auth/login.html", {} )


@login_required
def LogoutView(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    

    return render(request, "dashboard/auth/register.html", {
        "citizenship_statuses": CITIZENSHIP_STATUSES,
        "marital_choices": MARITAL_CHOICES,
        "program_types": PROGRAM_TYPES,
        "currencies": PREFERRED_CURRENCY,

    })

# View to handle password reset request
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        reset_email_url = request.POST.get('password_url')
        user = User.objects.filter(email=email).first()
        
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(f'/password-reset/{uid}/{token}/')
            print("Reset Email link: ", reset_email_url, "  -  ", reset_url)
            
            # send_password_reset_email(to_email=user.email, reset_link=reset_url)
            return JsonResponse({'success': 'Password reset email sent'})
        else:
            return JsonResponse({'error': 'Email address not found'}, status=404)
    return render(request, 'dashboard/auth/password_reset_form.html')

# View to handle password reset form submission
def password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    
                    return JsonResponse({'success': 'Password reset successfully'})
                else:
                    return JsonResponse({'error': 'Invalid token'}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'Invalid request'}, status=400)
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'dashboard/auth/password_reset_confirm.html')




def password_reset_complete(request):
    return render(request, 'dashboard/auth/password_reset_complete.html')


# ------------------------------------------------------------------------------------



# -------------------------------- DASHBOARD PAGES-------------------------------------
@login_required
def dashboard_home(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    return render(request, "dashboard/major/index.html", {
        "notifications": notifications,
         "notification_count": notifications.count(),
    } )

@login_required
def chart_analysis(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    return render(request, "dashboard/major/chart_analysis.html", {
        "notifications": notifications,
         "notification_count": notifications.count(),
    } )

@login_required
def fund_wallet(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    return render(request, "dashboard/major/fund_wallet.html", {
        "notifications": notifications,
         "notification_count": notifications.count(),
        "currencies": PREFERRED_CURRENCY
    } )

@login_required
def transactions(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    return render(request, "dashboard/major/transactions.html", {
        "notifications": notifications,
         "notification_count": notifications.count(),
    })


@login_required
def profile_details(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    
    return render(request, "dashboard/major/profile.html", {
        "notifications": notifications,  
        "notification_count": notifications.count(),
        })


@login_required
def profile_settings(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    return render(request, "dashboard/major/profile_settings.html", {
        "notifications": notifications,  
        "notification_count": notifications.count(),
        })



@login_required
def support_page(request):

    notifications = Notification.objects.filter(user=request.user).order_by("-id")[:5]
    read_notifications = Notification.objects.filter(user=request.user).filter(is_read=True).order_by("-id")[:5]

    supports = Support.objects.filter(user=request.user).order_by("-id")[:5]

    return render(request, "dashboard/major/support.html", {
        "supports": supports,"notifications": notifications, 
        "notification_count": notifications.count(),
        })
    


@login_required
def notification_page(request):
    notifications = Notification.objects.filter(user=request.user).filter(is_read=False).order_by("-id")[:5]
    all_notifications = Notification.objects.filter(user=request.user).order_by("is_read", "-id")[:5]

    return render(request, "dashboard/major/notifications.html", {
        "notifications": notifications, 
        "notification_count": notifications.count(), 
        "all_notifications": all_notifications
        })




# -------------------------------------------------------------------------------------





