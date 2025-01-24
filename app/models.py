from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import random
from datetime import datetime, timedelta

import string
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the broker app where email is the unique identifier for authentication.
    """
    GENDER_CHOICES = [
        ("Male", 'Male'),
        ("Female", 'Female'),
    ]
    PROGRAM_TYPES = [
        ("Short-Term", 'Short-Term'),
        ("Long-Term", 'Long-Term'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)  # Required
    last_name = models.CharField(max_length=50, blank=False)   # Required
    phone_number = models.CharField(max_length=15, unique=True, blank=False)  # Required
    date_of_birth = models.DateField(blank=True, null=True)

    preferred_currency = models.CharField(max_length=100, blank=True, null=True, default="$")

    profile_image = models.FileField(upload_to="profile/images", blank=True, null=True)

    address = models.TextField(blank=True, null=True)  
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)


    postal_code = models.CharField(max_length=100, blank=True, null=True)
    gender =  models.CharField(max_length=100, blank=True, null=True, choices=GENDER_CHOICES, default="Male")


    user_password_in_text = models.CharField(max_length=100, blank=True, null=True)

    annual_income = models.DecimalField(verbose_name="Annual Income", max_digits=12, decimal_places=2, default=0.00)
    citizenship_status = models.CharField(max_length=50, choices=[
        ('US Citizen', 'US Citizen'), 
        ('Non-US Citizen', 'Non-US Citizen')
    ], default='Non-US Citizen')
    
    # User Balances
    capital = models.DecimalField(verbose_name="Capital", max_digits=12, decimal_places=2, default=0.00)
    roi = models.DecimalField(verbose_name="ROI", max_digits=12, decimal_places=2, default=0.00)
    bonus = models.DecimalField(verbose_name="Bonus", max_digits=12, decimal_places=2, default=0.00)

    program_type = models.CharField(max_length=100, blank=True, null=True, choices=PROGRAM_TYPES, default="Short-Term")

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # User has verified KYC
    is_verified = models.BooleanField(verbose_name="KYC Verified", default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


    @property
    def available_balance(self):
        return self.capital + self.roi



    @property
    def get_profile_image_url(self):
        if self.profile_image:
            if self.profile_image.url.startswith("https"):
                return self.profile_image.url
            else:
                return "http://localhost:8000" + self.profile_image.url
        else:
            # Change this later
            return 'https://res.cloudinary.com/daf9tr3lf/image/upload/v1725024497/undraw_profile_male_oovdba.svg'
        
    @property
    def get_user_fullname(self):
        return str(self.first_name).capitalize() + " " + str(self.last_name).capitalize()


    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"


class KYC(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 

    PREFERRED_ID_TYPE = [
        ("Driver Licence", 'Driver Licence'),
        ("National ID", 'National ID'),
        ("Passport", 'Passport'),
    ]

    MARITAL_CHOICES = [
        ("Married", 'Married'),
        ("Single", 'Single'),
        ("Divorced", 'Divorced'),
    ]

    # GOVERNMENT ID 
    government_id_type = models.CharField(max_length=200, blank=True, null=True, choices=PREFERRED_ID_TYPE)
    government_id_number = models.CharField(max_length=200, blank=True, null=True)
    front_id_image = models.FileField(upload_to="identity/images", blank=True, null=True)
    back_id_image = models.FileField(upload_to="identity/images", blank=True, null=True)
    
    utility_bill = models.FileField(upload_to="identity/proof/utility", blank=True, null=True)
    
    ssn = models.CharField(max_length=500, blank=True, null=True)

    citizenship_status = models.CharField(max_length=50, choices=[
        ('US Citizen', 'US Citizen'), 
        ('Non-US Citizen', 'Non-US Citizen')
    ])

    class Meta:
        verbose_name_plural = "KYC"
        verbose_name = "KYC"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT REQUEST', 'DEPOSIT REQUEST'),
        ('WITHDRAWAL', 'WITHDRAWAL'),
    )

    TRANSACTION_STATUS = [
        ("Pending", "Pending"),
        ("Successful", "Successful"),
        ("Rejected", "Rejected")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 

    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='Pending')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Transactions"
        verbose_name = "Transaction"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("danger", "danger"),
        ("success", "success"),
        ("warning", "warning")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField()
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPES, verbose_name="Notification Type", help_text="Select the Notification Type. ")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.title}"

    class Meta:
        verbose_name_plural = "Notification"
        verbose_name = "Notifications"


class Support(models.Model):
    STATUS = [
        ("Pending", "Pending"),
        ("Fulfilled", "Fulfilled"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=400, blank=True, null=False)
    description = models.TextField(max_length=400, blank=True, null=False)
    image = models.FileField(upload_to='support/images/', null=True, blank=True)
    status = models.CharField(max_length=400, blank=True, null=False, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Support"
        verbose_name = "Support"

    def __str__(self):
        return f"Support for {self.user.email} - {self.subject}"


class Payment(models.Model):
    
    TRANSACTION_TYPES = (
        ('DEPOSIT REQUEST', 'DEPOSIT REQUEST'),
        ('WITHDRAWAL', 'WITHDRAWAL'),
    )
    PAYMENT_METHOD = [
        ("bank", "bank"),
        ("crypto", "crypto"),
        ("paypal", "paypal"),
        ("cashapp", "cashapp"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=400, blank=True, null=False, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    confirmation_receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    payment_method = models.CharField(max_length=400, blank=True, null=False, choices=PAYMENT_METHOD)
    is_tax = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self) -> str:
        return f"Received Payment from {self.user.email} in {self.payment_method}"



class AdminPaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ("CHOOSE WALLET", "CHOOSE WALLET"),
        ("BTC", "BTC"),
        ("ETH", "ETH"),
        ("CASH APP", "CASH APP"),
        ("PAYPAL", "PAYPAL")
    ]
    payment_type =  models.CharField(max_length=400, blank=True, null=False, choices=PAYMENT_TYPES)
    payment_address = models.CharField(max_length=400, blank=True, null=False)

    def __str__(self) -> str:
        return f"{self.payment_type}" 





