from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# from .constants import ACCOUNTS
from .serializers import SupportSerializer

from django.contrib.auth import update_session_auth_hash
import json

# from .email import (
#     send_beautiful_html_email_create_account, 
#     send_admin_mail, 
#     send_ordinary_user_mail,
#     send_mail_from_admin_to_user,
#     send_mail_for_payment_options,
#     send_contact_mail,
# )

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# from .helpers import check_email, is_valid_password

from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from django.shortcuts import render
from app.models import (
    KYC, 
    Payment, 
    CustomUser, 
    Notification, 
    Transaction, 
    Support
)

from django.contrib.auth import get_user_model

from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models import Support
# from .serializers import SupportSerializer, AccountActivationSerializer
from app.models import CustomUser
from django.contrib import messages

from django.conf import settings


# from .email import send_beautiful_html_email_create_user


User = CustomUser



@api_view(['POST'])
def register_api_view(request):
    if request.method == 'POST':

        print(request.data)

        required_fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'annual_income',
            'profile_image',
            'password', 'password_confirmation'
        ]

        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        email=request.data.get('email')       
        phone_number=request.data.get('phone_number')      
        annual_income=request.data.get('annual_income')
        program_type=request.data.get('program_type')

        country=request.data.get('country')
        state=request.data.get('state')
        postal_code=request.data.get('postal_code')
        date_of_birth=request.data.get('dob')
        city=request.data.get('city')
        address=request.data.get('address')
        citizenship_status=request.data.get('citizenship_status')
        profile_image=request.FILES.get('profile_image')
        password=request.data.get('password')
        preferred_currency = request.data.get('preferred_currency')
        
        password_confirmation=request.data.get('password_confirmation')

        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            return Response({"error": "User with email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != password_confirmation:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                annual_income=annual_income,
                city=city,
                postal_code=postal_code,
                date_of_birth=date_of_birth,
                address=address,
                country=country,
                state=state,
                profile_image=profile_image,
                citizenship_status=citizenship_status,
                program_type=program_type,
                user_password_in_text=password,
                preferred_currency=preferred_currency,
            )
            user.preferred_currency = preferred_currency
            user.set_password(password)
            user.save()

            


            # send_beautiful_html_email_create_user(
            #     bank_id=user.bank_id,
            #     account_details=f"Account Type: {user.preferred_account_type}, Balance: $0",
            #     to_email=user.email,
            # )

            # send_admin_mail(
            #     subject="New user Alert",
            #     message="Hi, a new user just registered and is ready for activation",
            # )

            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
@api_view(['POST'])
def change_password_api_view(request):
    data = request.data
    new_password = data.get("new_password")
    old_password = data.get("old_password")
    confirm_password = data.get("confirm_password")

    user = request.user

    if new_password != confirm_password:
        print("New passwords do not match.")
        return Response({'error': 'New passwords do not match.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user old_password is correct
    if not user.check_password(old_password):
        return Response({'error': 'Current password is incorrect.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.set_password(new_password)
    request.user.save()
    # Prevents logging out after password change
    update_session_auth_hash(request, request.user)


    return Response({'message': 'Password updated successfully.', 'success': True}, status=status.HTTP_201_CREATED)
















@api_view(['POST'])
def login_with_email_api(request):
    email = request.data.get('email')
    password = request.data.get('password')

    

    print(f"Details {email} {password}")

    try:
        user = CustomUser.objects.get(email=email)
        user = authenticate(request, email=user.email, password=password)
        if user is not None:
            login(request, user)

            # send_admin_mail(
            #     subject="Login Alert",
            #     message=f"User with email: {request.user.email} just logged into the app."
            # )
            # send_ordinary_user_mail(
            #     to_email=request.user.email,
            #     subject="Login Alert",
            #     message="We noticed a login attempt you made. Please know we take security very seriously at \
            #         Optimum Bank and we are dedicated to giving you the best banking experience."
            # )

            # Change the redirect url here if you change the dashboard
            return Response({'message': 'Login successful', 'redirect_url': '/dashboard'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials. Ensure your email and password are correct.'}, status=status.HTTP_401_UNAUTHORIZED)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)






@api_view(['POST'])
def update_profile_api_view(request):
    if request.method == "POST":
        data = request.data
        files = request.FILES

        user = request.user

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        state = data.get("state")
        city = data.get("city")
        country = data.get("country")
        address = data.get("address")
        profile_image = files.get("profile_image")

        user.first_name = first_name
        user.last_name = last_name
        user.state = state
        user.city = city
        user.country = country
        user.address = address

        if profile_image:
            user.profile_image = profile_image

        user.save()

        return Response({"message": "Profile updated successfully.", 'success': True}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Method is not allowed.", 'success': False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def support_api(request):
    serializer = SupportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        # send_admin_mail(
        #         subject="Login Alert",
        #         message=f"User with email {request.user.email} just logged into the app."
        # )
        # send_ordinary_user_mail(
        #     to_email=request.user.email,
        #         subject="Login Alert",
        #         message="We noticed a login attempt you made. Please know we take security very seriously at \
        #             Optimum Bank and we are dedicated to giving you the best banking experience."
        # )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_user_notification(request):
    # Bulk update all unread notifications for the user
    updated_count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return Response({
        "message": f"{updated_count} notifications have been marked as read!",
        "count": updated_count
    })

